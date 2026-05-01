import psycopg2
import datetime
from config import load_config

def get_all_results(cur):
    cur.execute("""
        SELECT gs.id, p.username, gs.score, gs.level_reached, gs.played_at
        FROM game_sessions gs
        JOIN players p ON p.id = gs.player_id
        ORDER BY gs.score DESC
    """)
    return cur.fetchall()

def get_or_create_player(cur, username):
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
    return cur.fetchone()[0]

def add_result(cur, username, score, level_reached):
    player_id = get_or_create_player(cur, username)
    cur.execute(
        "INSERT INTO game_sessions (player_id, score, level_reached, played_at) VALUES(%s, %s, %s, %s)",
        (player_id, score, level_reached, datetime.datetime.now())
    )

def launch(typ, username=None, score=None):
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                if typ == 1:
                    return get_all_results(cur)
                elif typ == 2:
                    add_result(cur, username, score, 0)
                    conn.commit()
    except Exception as e:
        print("launch error:", e)

if __name__ == '__main__':
    launch(1)