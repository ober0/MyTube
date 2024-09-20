from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task

# pip install eventlet celery
# celery -A MyTube worker --loglevel=info -P eventlet

@shared_task
def send_register_email(message, recipient_list):
    send_mail(
        'Регистрация на MyTube',
        str(message),
        settings.EMAIL_HOST_USER,
        recipient_list
    )
