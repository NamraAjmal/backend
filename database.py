import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")

with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS tasks (
                       id SERIAL PRIMARY KEY,
                       title TEXT NOT NULL,
                       done BOOLEAN NOT NULL
                    )""")
        cur.execute("SELECT COUNT(*) FROM tasks")
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute(
                "INSERT INTO tasks (title,done) VALUES('Buy Milk', false),('Pray',true),('Exercise',false)"
            )
    conn.commit()
