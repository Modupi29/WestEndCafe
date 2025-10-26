from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.
USER_TYPES = (
    ('Admin', 'Admin'),
    ('Customer', 'Customer'),
)
class CustomeUser(AbstractUser):

    user_type = models.CharField(choices=USER_TYPES, max_length=9, default='Customer')
    
    def __str__(self):
        return f"{self.username} - {self.user_type}"
    
class Profile(models.Model):
    user = models.OneToOneField(CustomeUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"