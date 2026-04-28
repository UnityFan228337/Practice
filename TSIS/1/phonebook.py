import psycopg2
from config import load_config
def get_all_nums(cur):
    cur.execute("SELECT * FROM phone_numbers")
    rows = cur.fetchall()
    return rows

def add_nums(cur):
    count = int(input("How many nums do you want to add?"))
    for i in range(count):
        surname = input("surname: ")
        name = input("name: ")
        num = input("num: ")
        while True:
            if len(num) > 11:
                print("longer that allowed. Try again")
                num = input("num: ")
            else:
                break
        try:
            cur.execute("INSERT INTO phone_numbers(surname, name, num) VALUES('"+surname+"', '"+name+"', '"+num+"')")
        except:
            print("error")

def change_nums(cur):
    count = int(input("How many do you wanna change?"))
    for i in range(count):
        searching_column = input("column for condition")
        what = input("condition ")
        replace_column = input("what column update?")
        new = input("new information?")
        try:
            cur.execute("UPDATE phone_numbers SET "+replace_column+" = '"+new+"' WHERE "+searching_column+" = '"+what+"'")
        except:
            print("error")
        
def get_some_nums(cur):
    columns = input("what's columns do we need to print?")
    if "," in columns:
        try:
            cur.execute("SELECT " + columns + " FROM phone_numbers")
            rows = cur.fetchall()
            return rows
        except:
                print("error")
    else:
        columns = columns.split()
    if columns[0] == "*" or columns[0].lower() == "all":
        cur.execute("SELECT * FROM phone_numbers")
        rows = cur.fetchall()
        return rows
    
    else:
        temp = ""
        for i in range(0, len(columns)-1):
            temp = temp + columns[i] + ", "
        temp += columns[-1]
        print(temp)
        try:
            cur.execute("SELECT " + temp + " FROM phone_numbers")
            rows = cur.fetchall()
            return rows
        except:
                print("error")

def delete_nums(cur):
    count = int(input("How many do you wanna delete?"))
    for i in range(count):
        column = input("By what's column we finding rows?")
        value = input("value of row")
        try:
            cur.execute("DELETE FROM phone_numbers WHERE "+column+" = '"+value+"'")
        except:
                print("error")

def import_from_csv(cur):
    f = input("name of file: ")
    try:
        with open(f, "r") as file:
            for line in file.readlines():
                data = line.strip().split(",")
                if len(data) >= 3:
                    surname = data[0].strip()
                    name = data[1].strip()
                    num = data[2].strip()
                    try:
                        cur.execute(f"INSERT INTO phone_numbers(surname, name, num) VALUES('{surname}', '{name}', '{num}')")
                    except:
                        print("error")
    
    except:
        print("error")

def search_by_pattern(cur):
    pattern = input("Search pattern: ")
    cur.execute("SELECT * FROM search_phone_records(%s)", (pattern,))
    for row in cur.fetchall():
        print(row)

def add_or_update(cur, conn):
    surname = input("surname: ")
    name = input("name: ")
    num = input("num: ")
    cur.callproc('upsert_contact', [surname, name, num])
    conn.commit()
    print("ok")

def paginated_view(cur):
    limit = int(input("limit: ") or "10") if input("show with limit? y/n: ").lower() == 'y' else 100
    offset = int(input("offset: ") or "0") if input("show with offset? y/n: ").lower() == 'y' else 0
    cur.execute("SELECT * FROM get_page(%s, %s)", (limit, offset))
    for row in cur.fetchall():
        print(row)

def launch():
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                menu = input("what's type of operation you will do? \n1. Get all nums\n2. Get some nums\n3. Add nums\n4. Update nums\n5. Delete nums\n6. Your own command\n7. Import from csv\n8. Search by pattern\n9. Add or update\n10. Paginated view\n")
                if menu == "1": 
                    for i in get_all_nums(cur):
                        print(i)
                if menu == "2": 
                    for i in get_some_nums(cur):
                        print(i)
                if menu == "3": 
                    add_nums(cur)
                    conn.commit()
                if menu == "4": 
                    change_nums(cur)
                    conn.commit()
                if menu == "5": 
                    delete_nums(cur)
                    conn.commit()
                if menu == "6": 
                    command = input()
                    cur.execute(command)
                    conn.commit()
                if menu == "7":
                    import_from_csv(cur)
                    conn.commit()
                if menu == "8":
                    search_by_pattern(cur)
                if menu == "9":
                    add_or_update(cur, conn)
                if menu == "10":
                    paginated_view(cur)
                
    except:
        print("error")

if __name__ == '__main__':
    getting = launch()