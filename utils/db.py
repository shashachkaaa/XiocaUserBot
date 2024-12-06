import sqlite3

connect = sqlite3.connect("db.db")
cursor = connect.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS settings(
	prefix STRING,
	name STRING,
	autoname STRING,
	tags_chat INT,
	tags STRING,
	dels_chat INT,
	dels STRING,
	version STRING,
	last_time STRING
)
""")
cursor.execute("""CREATE TABLE IF NOT EXISTS messages(
	message_id INT,
	user_id INT,
	message_text STRING
)
""")