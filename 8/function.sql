-- Функция: Поиск контактов по паттерну
CREATE OR REPLACE FUNCTION search_phone_records(pattern VARCHAR)
RETURNS TABLE(surname VARCHAR, name VARCHAR, num VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT * FROM phone_numbers
    WHERE surname ILIKE '%' || pattern || '%'
       OR name ILIKE '%' || pattern || '%'
       OR num ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- Процедура: Вставить новый или обновить существующий
CREATE OR REPLACE PROCEDURE upsert_contact(p_surname VARCHAR, p_name VARCHAR, p_num VARCHAR) AS $$
BEGIN
    IF EXISTS(SELECT 1 FROM phone_numbers WHERE surname = p_surname AND name = p_name) THEN
        UPDATE phone_numbers SET num = p_num WHERE surname = p_surname AND name = p_name;
    ELSE
        INSERT INTO phone_numbers(surname, name, num) VALUES(p_surname, p_name, p_num);
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Функция: Получить контакты с пагинацией
CREATE OR REPLACE FUNCTION get_page(lim INT, off INT)
RETURNS TABLE(surname VARCHAR, name VARCHAR, num VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT * FROM phone_numbers ORDER BY surname LIMIT lim OFFSET off;
END;
$$ LANGUAGE plpgsql;
