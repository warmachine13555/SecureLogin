import sqlite3
import hashlib
import socket
import threading
import pyotp
from totpgen import totp_register


def auth(c):
    for i in range(3):  # Versuche insgesamt 3 Anmeldeversuche
        c.send("Username: ".encode())
        username = c.recv(1024).decode()
        c.send("Password: ".encode())
        password = c.recv(1024).decode()
        password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

        if cur.fetchall():
            c.send("Login successful!".encode())
            if cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ? AND totp = 0", (username, password)):
                totp_register()

        else:
            c.send("Login failed! Please try again.".encode())

    c.send("Too many tries please retry later".encode())
    c.close()


