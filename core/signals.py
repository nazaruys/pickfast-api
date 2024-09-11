from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .utils import send_email

User = get_user_model()

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.verification_code:
        print('New User created!')
        subject = "Welcome to PickFast!"
        message = f"Hi {instance.username},\n\nThank you for signing up for our service. Here is your verification code: {instance.verification_code}"
        send_email(subject, message, [instance.email], from_name_email='PickFast <noreply@pick-fast.com>')