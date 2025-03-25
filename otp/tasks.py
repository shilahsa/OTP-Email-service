import json
from django.core.mail import EmailMessage
from django.conf import settings
from celery import shared_task


@shared_task
def send_verification_email(params):
    params = json.loads(params)
    code = params['code']
    email = params['email']

    subject = 'Verification code'
    email_body = f'Dear user, \nUse the following code to verify your account.\n\n {code}'
    message = EmailMessage(
        from_email=settings.EMAIL_HOST_USER,
        to=[email],
        subject=subject,
        body=email_body
    )

    message.send()

