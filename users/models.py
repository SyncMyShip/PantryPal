from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=20, unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users', default='no_profile_pic.jpg')

    def __str__(self):
        return f"Welcome {self.name}!"