# accounts/signals.py
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save, pre_save
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser  # CustomUser import

# Naye syntax se custom signals define
user_registered = Signal()
profile_updated = Signal()

# Built-in signals ke receivers - CustomUser ke liye
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Jab naya user create hota hai, automatically profile banayein
    """
    if created:
        print(f"New user created: {instance.username}")
        # UserProfile create karein agar needed
        # UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    New user ko welcome email bhejein
    """
    if created:
        print(f"Welcome email would be sent to: {instance.email}")

@receiver(pre_save, sender=CustomUser)
def user_pre_save(sender, instance, **kwargs):
    """
    User save hone se pehle kuch actions karein
    """
    print(f"User {instance.username} is about to be saved")

# Custom signal receivers
@receiver(user_registered)
def handle_user_registration(sender, **kwargs):
    user = kwargs.get('user')
    request = kwargs.get('request')
    print(f"Custom signal: User {user.username} registered via {request.method if request else 'unknown'}")