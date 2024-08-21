import psycopg2
from psycopg2.extras import RealDictCursor

# Centralized database connection function
def get_db_connection():
    return psycopg2.connect(
        dbname="yugioh_cards_db",
        user="postgres",
        password="postgres",
        host="localhost"
    )

def create_db():
    conn = get_db_connection()
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''
    CREATE TABLE IF NOT EXISTS cards (
        id TEXT PRIMARY KEY,
        name TEXT,
        card_type TEXT,
        attribute TEXT,
        level INTEGER,
        atk INTEGER,
        def_ INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def insert_card_into_db(card):
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
    INSERT INTO cards (id, name, card_type, attribute, level, atk, def_)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO NOTHING
    ''', (card.id, card.name, card.card_type, card.attribute, card.level, card.atk, card.def_))

    conn.commit()
    conn.close()

def query_db(query, args=(), one=False):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(query, args)
    rv = cur.fetchall()
    conn.close()
    return (rv[0] if rv else None) if one else rv
