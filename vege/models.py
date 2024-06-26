from django.db import models
from django.contrib.auth.models import User

class Receipe(models.Model):
     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
     receipe_name = models.CharField(max_length=100)
     receipe_desc = models.TextField()
     receipe_image = models.ImageField(upload_to="receipe")

class Profile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE)
     auth_token = models.CharField(max_length=100)
     is_verified = models.BooleanField(default=False)
     created_at = models.DateTimeField(auto_now_add=True)

     def __str__(self) -> str:
          return self.user.username
