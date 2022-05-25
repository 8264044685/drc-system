import string
import secrets
from django.conf import settings
from django.core.mail import send_mail


def send_otp(mobile_no, country_code="+91"):
    alphabet = string.digits
    otp = "".join(secrets.choice(alphabet) for i in range(4))
    print(f"mobile number {mobile_no} with otp is {otp}")
    return otp


def user_send_mail(user):
    subject = 'welcome to DRC world'
    message = f'Hi {user.username}, thank you for registering.'
    email_from = settings.EMAIL_HOST_USER
    email_list = [user.user_emails.filter(is_primary=True).last() if user.user_emails.filter(is_primary=True) else user.user_emails.all().last(),]

    print(subject)
    print(message)
    print(email_from)
    print(email_list)

    """
        if we uncomment this method then we need to add an email and 
        password into setting.py and also remove secure from email
        this is just for information.
    """ 
    
    # send_mail( subject, message, email_from, email_list )
