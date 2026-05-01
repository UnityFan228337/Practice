import psycopg2
from config import load_config

def connect(config=None):
    if config is None:
        config = load_config()
    return psycopg2.connect(**config)


if __name__ == '__main__':
    config = load_config()
    conn = connect(config)
    print('Connected to the PostgreSQL server.')
    conn.close()
