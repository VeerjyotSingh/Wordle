import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('words.db')
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL
)
""")

# Open the text file containing words
with open('words.txt', 'r') as file:
    words = file.readlines()

# Insert each word into the database
for word in words:
    word = word.strip()
    cursor.execute("INSERT INTO Words (word) VALUES (?)", (word,))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Words have been loaded into the database.")