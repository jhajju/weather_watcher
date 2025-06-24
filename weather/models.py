from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f"{self.name} ({self.user.username})"
    
    class Meta:
        verbose_name_plural = "Cities"
