import sqlite3
import hashlib
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("81.169.141.81", 8888))
#server.bind(("localhost", 8888))

server.listen()


def handle_connection(c):
    for i in range(3):  # Versuche insgesamt 3 Anmeldeversuche
        c.send("Username: ".encode())
        username = c.recv(1024).decode()
        c.send("Password: ".encode())
        password = c.recv(1024).decode()
        password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

        if cur.fetchall():
            c.send("Login successful!".encode())
            break  # Beenden Sie die Schleife, wenn die Anmeldung erfolgreich war
        else:
            c.send("Login failed! Please try again.".encode())

    c.send("Too many tries please retry later".encode())
    c.close()


while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()