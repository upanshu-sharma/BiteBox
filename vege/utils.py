from django.core.mail import send_mail
from django.conf import settings
import uuid

def send_verification_email(user):
    verification_code = str(uuid.uuid4())
    user.verification_code = verification_code
    user.save()

    subject = 'Verify your email'
    message = f'Please click the link to verify your email: {settings.SITE_URL}/verify/{verification_code}/'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )
