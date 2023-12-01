import sqlite3

# setting database path
db_path = 'database/pong.db'
conn = sqlite3.connect(db_path) # connecting
c = conn.cursor() # cursor to allow sql statements
# creating table leader_board
c.execute("CREATE TABLE IF NOT EXISTS leader_board"
          "(user_name TEXT PRIMARY KEY, score INTEGER, selected_ai_speed TEXT)")

# inserting some base data
c.execute("INSERT INTO leader_board "
          "values (?, ?, ?)", ("John", 40529391, "not working"))

# adding and closing
conn.commit()
conn.close()
