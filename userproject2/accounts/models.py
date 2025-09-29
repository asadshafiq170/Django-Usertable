from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=11, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username

    # Example Model Function
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def is_adult(self):
        """Check if user is 18+"""
        if self.date_of_birth:
            from datetime import date
            age = date.today().year - self.date_of_birth.year
            return age >= 18
        return False


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  # CustomUser use karein
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    # Example Model Function
    def short_bio(self):
        """bio ko short kar ke dikhana"""
        return self.bio[:50] + "..." if len(self.bio) > 50 else self.bio
