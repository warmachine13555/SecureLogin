import sqlite3
import hashlib
import socket
import threading
import authentication


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("81.169.141.81", 8888))
#server.bind(("localhost", 8888))

server.listen()

authentication()



while True:
    client, addr = server.accept()
    threading.Thread(target=handle_connection, args=(client,)).start()