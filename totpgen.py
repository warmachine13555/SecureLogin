import time
import pyotp
import qrcode
import socket
import threading



key = pyotp.random_base32()  # Generate a random base32 key

print(key)

totp = pyotp.TOTP(key)

uri = totp.provisioning_uri(name="Benjamin", issuer_name="Online Banking")

# Manually append the TOTP period to the URI
uri += "&period=30"

qrcode.make(uri).save("totp.png")

totp = pyotp.TOTP(key)

while True:
    print(totp.verify(input("Enter code: ")))