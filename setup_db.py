import sqlite3

if __name__ == '__main__':
    try:
        open('db.db', 'r').close()
    except FileNotFoundError:
        db = sqlite3.connect('db.db')
        cursor = db.cursor()
        with open('create_db.sql', 'r') as f:
            cursor.execute(f.read())