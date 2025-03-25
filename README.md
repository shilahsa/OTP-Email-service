# OTP-Email-service
you can send email code and verify user email

# Test connection SMTP 
CMD : telnet EMAIL_HOST_USER EMAIL_PORT 

# Test connection SMTP 
python shell :
from django.core.mail import send_mail
send_mail(
    'Test Subject',
    'This is a test email.',
    'EMAIL_HOST_USER',
    [''], #real email
    fail_silently=False,
)
