from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserWall(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wall")

    def __str__(self):
        return f"{self.user.username}'s wall"
    
class Post(models.Model):
    wall = models.ForeignKey(UserWall, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to="post_images", blank=True)

    def __str__(self):
        return f"Post on {self.wall.user.username}'s wall"