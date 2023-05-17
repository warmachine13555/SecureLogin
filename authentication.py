import sqlite3
import hashlib
import pyotp
import qrcode


def auth(c):
    for i in range(3):
        c.send("Username: ".encode())
        username = c.recv(1024).decode()
        c.send("Password: ".encode())
        password = c.recv(1024)
        password = hashlib.sha256(password).hexdigest()

        conn = sqlite3.connect("userdata.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))

        if cur.fetchall():
            c.send("Username and password correct! Now you need to verify your MFA code. Look on your Phone please.".encode())
            if cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ? AND totp = 0", (username,
                                                                                                       password)):
                key = pyotp.random_base32()

                print(key)

                totp = pyotp.TOTP(key)

                uri = totp.provisioning_uri(name=username, issuer_name="Online Banking")

                uri += "&period=30"

                qrcode.make(uri).save("totp.png")

                totp = pyotp.TOTP(key)

                c.send("Enter MFA Code: ".encode())
                mfa_code = c.recv(1024).decode().strip()
                verify = totp.verify(mfa_code)
                print(verify)

                if verify:
                    loginsuccessful(c)

                    conn = sqlite3.connect("userdata.db")
                    cur = conn.cursor()
                    cur.execute("UPDATE userdata SET totp = ? WHERE username = ?", (key, username))
                    conn.commit()

                    break
                if not verify:
                    c.send("MFA Code invalid. Please try again.".encode())
        else:
            c.send("Login failed! Please try again.".encode())

    c.send("Too many tries please retry later".encode())
    c.close()



def loginsuccessful(c):
    c.send("MFA Code valid. Login successful!".encode())