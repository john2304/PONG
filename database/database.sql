import sqlite3

db_file = "sqlite3.db"

sql_script = """
DROP TABLE if EXIST albums;

CREATE TABLE user_info (
	id VARCHAR(11) NOT NULL,
	title VARCHAR(150),
	wins VARCHAR(100),
	loss VARCHAR(100),
	PRIMARY KEY (id),
	UNIQUE (id),
);
"""

# Connect to the database and execute the SQL script
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.executescript(sql_script

conn.commit()
conn.close()