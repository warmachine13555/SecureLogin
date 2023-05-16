import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("81.169.141.81", 8888))

server.listen()


def handle_connection(c):
    c.send("Username: ".encode())
    username = c.recv(1024).decode()
    c.send("Password: ".encode())
    password = c.recv(1024)
    password = hashlib.sha256(password).hexdigest()

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

    if cur.fetchall():
        c.send("Login succesful!".encode())
    else:
        c.send("Login failed!".encode())

while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()