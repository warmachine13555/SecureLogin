import pyotp
import qrcode




key = pyotp.random_base32()

print(key)

totp = pyotp.TOTP(key)

uri = totp.provisioning_uri(name="Benjamin", issuer_name="Online Banking")


uri += "&period=30"

qrcode.make(uri).save("totp.png")

totp = pyotp.TOTP(key)

while True:
    print(totp.verify(input("Enter code: ")))