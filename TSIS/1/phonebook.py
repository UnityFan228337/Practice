import csv
import json
import os
from datetime import datetime

import psycopg2
from connect import connect
from config import load_config

GROUPS = ['Family', 'Work', 'Friend', 'Other']
PHONE_TYPES = ['home', 'work', 'mobile']

def normalize_group(group_name):
    if not group_name:
        return 'Other'
    normalized = group_name.strip().title()
    return normalized if normalized in GROUPS else 'Other'

def normalize_phone_type(phone_type):
    if not phone_type:
        return 'mobile'
    normalized = phone_type.strip().lower()
    return normalized if normalized in PHONE_TYPES else 'mobile'

def parse_date(date_text):
    if not date_text:
        return None
    try:
        return datetime.strptime(date_text.strip(), '%Y-%m-%d').date()
    except ValueError:
        return None

def contact_display(contact):
    phones = contact['phones']
    if isinstance(phones, str):
        try:
            phones = json.loads(phones)
        except json.JSONDecodeError:
            phones = []

    phone_lines = []
    for phone in phones or []:
        if isinstance(phone, dict):
            phone_lines.append(f"{phone.get('type', '')}:{phone.get('phone', '')}")

    date_added = contact['date_added']
    if isinstance(date_added, datetime):
        date_added = date_added.strftime('%Y-%m-%d %H:%M')

    return (
        f"{contact['surname']} {contact['name']} | email: {contact['email'] or '-'} | "
        f"birthday: {contact['birthday'] or '-'} | group: {contact['group_name'] or 'Other'} | "
        f"added: {date_added}\n    phones: {', '.join(phone_lines) if phone_lines else '-'}"
    )

def fetch_contacts(cur, where_clause='', params=None, order_by='c.surname, c.name', limit=None, offset=None):
    params = list(params or [])
    sql = '''
    SELECT
        c.id,
        c.surname,
        c.name,
        c.email,
        c.birthday,
        COALESCE(g.name, 'Other') AS group_name,
        c.date_added,
        COALESCE(
            json_agg(json_build_object('phone', p.phone, 'type', p.type))
            FILTER (WHERE p.id IS NOT NULL),
            '[]'
        ) AS phones
    FROM contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    '''

    if where_clause:
        sql += ' WHERE ' + where_clause

    sql += f' GROUP BY c.id, g.name ORDER BY {order_by}'

    if limit is not None:
        sql += ' LIMIT %s'
        params.append(limit)
    if offset is not None:
        sql += ' OFFSET %s'
        params.append(offset)

    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    contacts = []
    for row in rows:
        contacts.append({
            'id': row[0],
            'surname': row[1],
            'name': row[2],
            'email': row[3],
            'birthday': row[4].isoformat() if row[4] else None,
            'group_name': row[5],
            'date_added': row[6],
            'phones': row[7],
        })
    return contacts

def get_or_create_group_id(cur, group_name):
    normalized = normalize_group(group_name)
    cur.execute('INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING', (normalized,))
    cur.execute('SELECT id FROM groups WHERE name = %s', (normalized,))
    return cur.fetchone()[0]

def find_contact_id(cur, surname, name):
    cur.execute('SELECT id FROM contacts WHERE surname = %s AND name = %s', (surname, name))
    row = cur.fetchone()
    return row[0] if row else None

def parse_full_name(full_name):
    parts = [part.strip() for part in full_name.split() if part.strip()]
    if not parts:
        return None, None
    if len(parts) == 1:
        return parts[0], ''
    return parts[0], ' '.join(parts[1:])

def insert_or_update_contact(cur, surname, name, email=None, birthday=None, group_name=None, phones=None, overwrite=False):
    group_id = get_or_create_group_id(cur, group_name)
    birthday_value = parse_date(birthday) if isinstance(birthday, str) else birthday
    if overwrite:
        cur.execute(
            '''UPDATE contacts
               SET email = %s,
                   birthday = %s,
                   group_id = %s
               WHERE surname = %s AND name = %s
               RETURNING id''',
            (email, birthday_value, group_id, surname, name),
        )
        row = cur.fetchone()
        if row:
            contact_id = row[0]
            cur.execute('DELETE FROM phones WHERE contact_id = %s', (contact_id,))
        else:
            cur.execute(
                '''INSERT INTO contacts(surname, name, email, birthday, group_id)
                   VALUES (%s, %s, %s, %s, %s)
                   RETURNING id''',
                (surname, name, email, birthday_value, group_id),
            )
            contact_id = cur.fetchone()[0]
    else:
        cur.execute(
            '''INSERT INTO contacts(surname, name, email, birthday, group_id)
               VALUES (%s, %s, %s, %s, %s)
               ON CONFLICT (surname, name) DO UPDATE
               SET email = EXCLUDED.email,
                   birthday = EXCLUDED.birthday,
                   group_id = EXCLUDED.group_id
               RETURNING id''',
            (surname, name, email, birthday_value, group_id),
        )
        contact_id = cur.fetchone()[0]
    for phone, phone_type in (phones or []):
        normalized_type = normalize_phone_type(phone_type)
        if phone:
            cur.execute(
                '''INSERT INTO phones(contact_id, phone, type)
                   VALUES (%s, %s, %s)
                   ON CONFLICT (contact_id, phone, type) DO NOTHING''',
                (contact_id, phone.strip(), normalized_type),
            )
    return contact_id

def list_all_contacts(cur):
    contacts = fetch_contacts(cur)
    if not contacts:
        print('No contacts found.')
        return
    print('\nAll contacts:')
    for contact in contacts:
        print(contact_display(contact))
        print()

def search_contacts_by_pattern(cur):
    pattern = input('Search pattern: ').strip()
    if not pattern:
        print('Search pattern cannot be empty.')
        return
    cur.execute('SELECT * FROM search_contacts(%s)', (pattern,))
    rows = cur.fetchall()
    if not rows:
        print('No contacts matched the pattern.')
        return
    for row in rows:
        contact = {
            'surname': row[1],
            'name': row[2],
            'email': row[3],
            'birthday': row[4].isoformat() if row[4] else None,
            'group_name': row[5],
            'date_added': row[6],
            'phones': row[7],
        }
        print(contact_display(contact))
        print()

def search_contacts_by_email(cur):
    email_search = input('Email search term: ').strip()
    if not email_search:
        print('Search term cannot be empty.')
        return
    contacts = fetch_contacts(cur, 'c.email ILIKE %s', ['%' + email_search + '%'])
    if not contacts:
        print('No email matches found.')
        return
    for contact in contacts:
        print(contact_display(contact))
        print()

def filter_contacts_by_group(cur):
    cur.execute('SELECT name FROM groups ORDER BY name')
    groups = [row[0] for row in cur.fetchall()]
    print('Available groups:', ', '.join(groups))
    group_name = input('Choose group: ').strip()
    normalized = normalize_group(group_name)
    contacts = fetch_contacts(cur, 'g.name = %s', [normalized])
    if not contacts:
        print(f'No contacts found in group {normalized}.')
        return
    for contact in contacts:
        print(contact_display(contact))
        print()

def sort_contacts(cur):
    sort_options = {
        '1': ('c.surname, c.name', 'name'),
        '2': ('c.birthday NULLS LAST, c.surname, c.name', 'birthday'),
        '3': ('c.date_added DESC', 'date added'),
    }
    print('Sort by: 1) Name 2) Birthday 3) Date added')
    choice = input('Choose sort option: ').strip()
    order_by = sort_options.get(choice, sort_options['1'])[0]
    contacts = fetch_contacts(cur, order_by=order_by)
    if not contacts:
        print('No contacts available.')
        return
    for contact in contacts:
        print(contact_display(contact))
        print()

def paginated_contacts(cur):
    try:
        page_size = int(input('Page size [default 5]: ').strip() or 5)
    except ValueError:
        page_size = 5
    order_by = 'c.surname, c.name'
    offset = 0
    while True:
        contacts = fetch_contacts(cur, order_by=order_by, limit=page_size, offset=offset)
        if not contacts:
            if offset == 0:
                print('No contacts found.')
            else:
                print('No more contacts.')
            break
        print(f'--- Showing {offset + 1} to {offset + len(contacts)} ---')
        for contact in contacts:
            print(contact_display(contact))
            print()
        command = input('Command [next, prev, quit]: ').strip().lower()
        if command == 'next':
            offset += page_size
        elif command == 'prev':
            offset = max(0, offset - page_size)
        else:
            break

def add_new_contact(cur):
    surname = input('Surname: ').strip()
    name = input('Name: ').strip()
    email = input('Email: ').strip() or None
    birthday = input('Birthday (YYYY-MM-DD): ').strip() or None
    group_name = input('Group [Family/Work/Friend/Other]: ').strip() or 'Other'
    phones = []
    while True:
        phone = input('Phone number (leave blank to stop): ').strip()
        if not phone:
            break
        phone_type = input('Phone type [home/work/mobile]: ').strip() or 'mobile'
        phones.append((phone, phone_type))
    insert_or_update_contact(cur, surname, name, email, birthday, group_name, phones)
    print('Contact added or updated successfully.')

def update_contact(cur):
    full_name = input('Contact full name (surname name): ').strip()
    surname, name = parse_full_name(full_name)
    if not surname:
        print('Invalid name.')
        return
    contact_id = find_contact_id(cur, surname, name)
    if not contact_id:
        print('Contact not found.')
        return
    cur.execute('SELECT email, birthday, COALESCE(g.name, ''Other'') FROM contacts c LEFT JOIN groups g ON g.id = c.group_id WHERE c.id = %s', (contact_id,))
    current = cur.fetchone()
    current_email, current_birthday, current_group = current
    email = input(f'Email [{current_email or ""}]: ').strip() or current_email
    birthday = input(f'Birthday [{current_birthday or ""}] (YYYY-MM-DD): ').strip() or (current_birthday.isoformat() if current_birthday else None)
    group_name = input(f'Group [{current_group}]: ').strip() or current_group
    insert_or_update_contact(cur, surname, name, email, birthday, group_name, [], overwrite=True)
    print('Contact updated successfully.')

def delete_contact(cur):
    full_name = input('Contact full name to delete (surname name): ').strip()
    surname, name = parse_full_name(full_name)
    if not surname:
        print('Invalid name.')
        return
    contact_id = find_contact_id(cur, surname, name)
    if not contact_id:
        print('Contact not found.')
        return
    cur.execute('DELETE FROM contacts WHERE id = %s', (contact_id,))
    print('Contact deleted.')

def add_phone_to_contact(cur):
    full_name = input('Contact full name (surname name): ').strip()
    phone = input('Phone number: ').strip()
    phone_type = input('Phone type [home/work/mobile]: ').strip() or 'mobile'
    try:
        cur.callproc('add_phone', [full_name, phone, normalize_phone_type(phone_type)])
        print('Phone added successfully.')
    except psycopg2.Error as exc:
        print('Error adding phone:', exc.pgerror or exc)

def move_contact_to_group(cur):
    full_name = input('Contact full name (surname name): ').strip()
    group_name = input('Target group [Family/Work/Friend/Other]: ').strip() or 'Other'
    try:
        cur.callproc('move_to_group', [full_name, normalize_group(group_name)])
        print('Contact moved to group successfully.')
    except psycopg2.Error as exc:
        print('Error moving contact:', exc.pgerror or exc)

def export_to_json(cur):
    contacts = fetch_contacts(cur)
    if not contacts:
        print('No contacts to export.')
        return
    out_path = input('JSON file name [contacts_export.json]: ').strip() or 'contacts_export.json'
    with open(out_path, 'w', encoding='utf-8') as file:
        json.dump(contacts, file, ensure_ascii=False, indent=2, default=str)
    print(f'Exported {len(contacts)} contacts to {out_path}')

def import_from_json(cur):
    path = input('JSON file name: ').strip()
    if not path or not os.path.exists(path):
        print('File not found.')
        return
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    for contact in data:
        surname = contact.get('surname', '').strip()
        name = contact.get('name', '').strip()
        if not surname or not name:
            continue
        existing_id = find_contact_id(cur, surname, name)
        if existing_id:
            decision = input(f'Contact {surname} {name} already exists. Skip or overwrite? [s/o]: ').strip().lower()
            if decision != 'o':
                continue
            overwrite = True
        else:
            overwrite = False
        phones = []
        for phone in contact.get('phones', []):
            if isinstance(phone, dict):
                phones.append((phone.get('phone', '').strip(), phone.get('type', 'mobile')))
        insert_or_update_contact(
            cur,
            surname,
            name,
            contact.get('email'),
            contact.get('birthday'),
            contact.get('group_name') or contact.get('group'),
            phones,
            overwrite=overwrite,
        )
    print('JSON import completed.')

def import_from_csv(cur):
    source_path = input('CSV file name: ').strip()
    if not source_path or not os.path.exists(source_path):
        print('File not found.')
        return
    with open(source_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        if reader.fieldnames and 'surname' in [h.lower() for h in reader.fieldnames]:
            for row in reader:
                surname = row.get('surname', '').strip()
                name = row.get('name', '').strip()
                email = row.get('email', '').strip() or None
                birthday = row.get('birthday', '').strip() or None
                group_name = row.get('group', '').strip() or 'Other'
                phones = []
                idx = 1
                while True:
                    phone = row.get(f'phone{idx}', '').strip()
                    if not phone:
                        break
                    phone_type = row.get(f'phone{idx}_type', '').strip() or 'mobile'
                    phones.append((phone, phone_type))
                    idx += 1
                insert_or_update_contact(cur, surname, name, email, birthday, group_name, phones)
        else:
            file.seek(0)
            for line in file:
                columns = [value.strip() for value in line.strip().split(',') if value.strip()]
                if len(columns) < 3:
                    continue
                surname, name, phone = columns[:3]
                insert_or_update_contact(cur, surname, name, None, None, 'Other', [(phone, 'mobile')])
    print('CSV import completed.')

def initialize_database(conn):
    base_dir = os.path.dirname(__file__)
    schema_path = os.path.join(base_dir, 'schema.sql')
    procedures_path = os.path.join(base_dir, 'procedures.sql')
    with open(schema_path, 'r', encoding='utf-8') as schema_file:
        schema_sql = schema_file.read()
    with open(procedures_path, 'r', encoding='utf-8') as proc_file:
        procedures_sql = proc_file.read()
    with conn.cursor() as cur:
        cur.execute(schema_sql)
        cur.execute(procedures_sql)
    conn.commit()
    print('Database schema and stored procedures initialized.')

def show_menu():
    print('\n=== Extended PhoneBook Menu ===')
    print('1) List all contacts')
    print('2) Search contacts by pattern')
    print('3) Search contacts by email')
    print('4) Filter contacts by group')
    print('5) Sort contacts')
    print('6) Paginated contacts')
    print('7) Add contact')
    print('8) Update contact')
    print('9) Delete contact')
    print('10) Add phone to contact')
    print('11) Move contact to group')
    print('12) Export contacts to JSON')
    print('13) Import contacts from JSON')
    print('14) Import contacts from CSV')
    print('15) Initialize database schema and procedures')
    print('0) Quit')

def main():
    config = load_config()
    conn = connect(config)
    try:
        with conn:
            with conn.cursor() as cur:
                while True:
                    show_menu()
                    choice = input('Select an option: ').strip()
                    if choice == '1':
                        list_all_contacts(cur)
                    elif choice == '2':
                        search_contacts_by_pattern(cur)
                    elif choice == '3':
                        search_contacts_by_email(cur)
                    elif choice == '4':
                        filter_contacts_by_group(cur)
                    elif choice == '5':
                        sort_contacts(cur)
                    elif choice == '6':
                        paginated_contacts(cur)
                    elif choice == '7':
                        add_new_contact(cur)
                        conn.commit()
                    elif choice == '8':
                        update_contact(cur)
                        conn.commit()
                    elif choice == '9':
                        delete_contact(cur)
                        conn.commit()
                    elif choice == '10':
                        add_phone_to_contact(cur)
                        conn.commit()
                    elif choice == '11':
                        move_contact_to_group(cur)
                        conn.commit()
                    elif choice == '12':
                        export_to_json(cur)
                    elif choice == '13':
                        import_from_json(cur)
                        conn.commit()
                    elif choice == '14':
                        import_from_csv(cur)
                        conn.commit()
                    elif choice == '15':
                        initialize_database(conn)
                    elif choice == '0':
                        break
                    else:
                        print('Unknown option. Please choose a number from 0 to 15.')
    finally:
        conn.close()


if __name__ == '__main__':
    main()
