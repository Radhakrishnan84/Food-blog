from django.contrib.auth.models import User
from django.db import models

class AccountProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile/', default='default.png', blank=True, null=True)
    bio = models.TextField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username