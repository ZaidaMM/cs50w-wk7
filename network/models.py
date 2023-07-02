from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return{
            'id': self.id,
            'body': self.body,
            'timestamp': self.timestamp.strftime('%b %d %Y, %I:%M %p')

        }
    
class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', blank=True)

    def __str__(self):
         return f" {self.follower} follows {self.following}"