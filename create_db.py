import sqlite3
db_path = 'database/pong.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS leader_board"
          "(user_name TEXT PRIMARY KEY, score INTEGER)")

c.execute("CREATE TABLE IF NOT EXISTS users"
          "(user_name TEXT PRIMARY KEY, password TEXT, verified INTEGER)")

c.execute("INSERT INTO users "
           "values (?, ?, ?)", ("me", "me_irl", 0))

c.execute("INSERT INTO leader_board "
          "values (?, ?)", ("me", 100))

conn.commit()
conn.close()
