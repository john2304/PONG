import sqlite3
db_path = 'database/pong.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS leader_board"
          "(user_name TEXT PRIMARY KEY, score INTEGER, selected_ai_speed TEXT)")

c.execute("INSERT INTO leader_board "
          "values (?, ?, ?)", ("me", 100, "ezy"))

conn.commit()
conn.close()
