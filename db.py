import sqlite3
db = sqlite3.connect('bot.db')
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER,
    username TEXT,
    status INTEGER,
    admin_id INTEGER)
    """)


#for value in sql.execute("SELECT * FROM users_data"):
 #   print(value)

#sql.execute(f"ALTER TABLE results ADD COLUMN que1 TEXT"
#sql.execute("""ALTER TABLE results ADD COLUMN que5""")
#sql.execute("""DROP TABLE users""")
'''
rows = sql.execute('SELECT * FROM users_data').fetchall()
for row in rows:
    print(row)
'''