import sqlite3
import hashlib

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    totp VARCHAR(255) NOT NULL
)
""")

username1, password1 = "mike", hashlib.sha256("mikepassword".encode()).hexdigest()
username2, password2 = "anna", hashlib.sha256("annapassword".encode()).hexdigest()
username3, password3 = "ben", hashlib.sha256("benpassword".encode()).hexdigest()
username4, password4 = "andi", hashlib.sha256("andipassword".encode()).hexdigest()

totp_empty = ""

cur.execute("INSERT INTO userdata (username, password, totp) VALUES (?, ?, ?)", (username1, password1, totp_empty))
cur.execute("INSERT INTO userdata (username, password, totp) VALUES (?, ?, ?)", (username2, password2, totp_empty))
cur.execute("INSERT INTO userdata (username, password, totp) VALUES (?, ?, ?)", (username3, password3, totp_empty))
cur.execute("INSERT INTO userdata (username, password, totp) VALUES (?, ?, ?)", (username4, password4, totp_empty))

conn.commit()