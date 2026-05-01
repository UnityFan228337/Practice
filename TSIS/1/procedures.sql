CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR) AS $$
DECLARE
    contact_id INTEGER;
BEGIN
    SELECT id INTO contact_id
    FROM contacts
    WHERE concat_ws(' ', surname, name) = p_contact_name
    LIMIT 1;

    IF contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    IF p_type NOT IN ('home', 'work', 'mobile') THEN
        RAISE EXCEPTION 'Invalid phone type %', p_type;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES (contact_id, p_phone, p_type)
    ON CONFLICT (contact_id, phone, type) DO NOTHING;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR) AS $$
DECLARE
    group_id INTEGER;
    contact_id INTEGER;
BEGIN
    INSERT INTO groups(name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;

    SELECT id INTO group_id FROM groups WHERE name = p_group_name LIMIT 1;

    SELECT id INTO contact_id
    FROM contacts
    WHERE concat_ws(' ', surname, name) = p_contact_name
    LIMIT 1;

    IF contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    UPDATE contacts
    SET group_id = group_id
    WHERE id = contact_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INTEGER,
    surname VARCHAR,
    name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    date_added TIMESTAMP,
    phones JSON
) AS $$
BEGIN
    RETURN QUERY
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
    WHERE c.surname ILIKE '%' || p_query || '%'
       OR c.name ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, g.name
    ORDER BY c.surname, c.name;
END;
$$ LANGUAGE plpgsql;
