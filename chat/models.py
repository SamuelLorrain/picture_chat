from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Room(models.Model):
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='creator')
    admin = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='admin')
    participants = models.ManyToManyField(to=User)
    name = models.CharField(max_length=250)
    # created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    room = models.ForeignKey(to=Room, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(null=True, blank=True)
    # created_at = models.DateTimeField(default=datetime.now())

