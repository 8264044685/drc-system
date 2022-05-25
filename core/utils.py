import string
import secrets



def send_otp(mobile_no, country_code="+91"):
    alphabet = string.digits
    otp = "".join(secrets.choice(alphabet) for i in range(4))
    print(f"mobile number {mobile_no} with otp is {otp}")
    return otp
