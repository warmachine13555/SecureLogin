import sqlite3
import hashlib
import socket
import threading
import pyotp
import qrcode
from totpgen import totp_register


def auth(c):
    for i in range(3):  # Versuche insgesamt 3 Anmeldeversuche
        c.send("Username: ".encode())
        username = c.recv(1024).decode()
        c.send("Password: ".encode())
        password = c.recv(1024)
        password = hashlib.sha256(password).hexdigest()

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

        if cur.fetchall():
            c.send("Login successful!".encode())
            if cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ? AND totp = 0", (username,
                                                                                                     password)):
                key = pyotp.random_base32()  # Generate a random base32 key

                print(key)

                totp = pyotp.TOTP(key)

                uri = totp.provisioning_uri(name="Benjamin", issuer_name="Online Banking")

                # Manually append the TOTP period to the URI
                uri += "&period=30"

                qrcode.make(uri).save("totp.png")

                totp = pyotp.TOTP(key)

                while True:
                    c.send("Enter MFA Code: ".encode())
                    mfa_code = c.recv(1024).decode()
                    verify = totp.verify(mfa_code)
                    print(verify)

        else:
            c.send("Login failed! Please try again.".encode())

    c.send("Too many tries please retry later".encode())
    c.close()


