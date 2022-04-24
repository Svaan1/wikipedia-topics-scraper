import sqlite3

con = sqlite3.connect('topics.db')
cur = con.cursor()

def create_tables():
    cur.execute('''CREATE TABLE IF NOT EXISTS "Topics"
    ("id" INTEGER,
    "name" TEXT NOT NULL UNIQUE,
    "done" INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY("id"))
    ''')
    cur.execute('''CREATE TABLE IF NOT EXISTS "Relations"
    ("root_id" INTEGER NOT NULL,
    "end_id" INTEGER NOT NULL,
    FOREIGN KEY("root_id") REFERENCES Topics("id"),
    FOREIGN KEY("end_id") REFERENCES Topics("id"),
    unique ("root_id", "end_id"))
    ''')

def add_to_topics_table(topic):
    try: cur.execute('''
    INSERT INTO "Topics"
    ("name")
    VALUES (?)
    ''', (topic,))
    except:
        print("An error ocurred, probably", topic, "is already on topics table.")

    return find_id_from_topics_table(topic)

def find_id_from_topics_table(topic):
    cur.execute('''
    SELECT id FROM "Topics" WHERE name=?
    ''', (topic,))

    return cur.fetchone()

def add_to_relations_table(starting_topic, ending_topic):
    
    root = find_id_from_topics_table(starting_topic)[0]
    end = find_id_from_topics_table(ending_topic)[0]

    try: cur.execute('''
    INSERT INTO "Relations"
    ("root_id", "end_id")
    VALUES (?, ?)
    ''', (root, end, ))
    except:
        print("An error ocurred, probably a relation between",starting_topic, ending_topic, "already exists on relations table")

def count_topics():
    cur.execute('''
    SELECT COUNT(*) FROM "Topics";
    ''')
    return cur.fetchone()[0]

def find_next_undone_topic():
    cur.execute('''
    SELECT name FROM "Topics" WHERE done=0
    ''')
    return cur.fetchone()[0]

def set_as_done(topic):
    cur.execute('''
    UPDATE "Topics" SET done = 1 WHERE name = ?
    ''', (topic,))