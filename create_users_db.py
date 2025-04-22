import sqlite3

# Connect to or create the database
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create a 'users' table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("✅ users.db created with 'users' table.")
