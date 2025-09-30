from django.dispatch import Signal, receiver
from django.db.models.signals import post_save, pre_save
from .models import CustomUser

# Custom signals
user_registered = Signal()
profile_updated = Signal()


# Built-in signals
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(f"New user created: {instance.username}")


@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        print(f"Welcome email would be sent to: {instance.email}")


@receiver(pre_save, sender=CustomUser)
def user_pre_save(sender, instance, **kwargs):
    print(f"User {instance.username} is about to be saved")


# Custom signal
@receiver(user_registered)
def handle_user_registration(sender, **kwargs):
    user = kwargs.get('user')
    request = kwargs.get('request')
    print(f"Custom signal: User {user.username} registered via {request.method if request else 'unknown'}")
