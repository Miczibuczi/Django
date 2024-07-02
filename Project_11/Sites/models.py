from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class UserWall(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wall")

    def __str__(self):
        return f"{self.user.username}'s wall"
    
class Fanpage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fanpage")
    fanpage_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.fanpage_name
    
class Post(models.Model):
    wall = models.ForeignKey(UserWall, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    fanpage = models.ForeignKey(Fanpage, on_delete=models.CASCADE, related_name="posts", null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.FileField(upload_to="post_images", blank=True)

    def save(self, *args, **kwargs):
        if self.wall and self.fanpage:
            raise ValueError("A post cannot belong to both UserWall and Fanpage.")
        elif not self.wall and not self.fanpage:
            raise ValueError("A post must belong to either UserWall or Fanpage")
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)


    def __str__(self):
        if self.wall:
            return f"Post on {self.wall.user.username}'s wall"
        elif self.fanpage:
            return f"Post on {self.fanpage.fanpage_name}"
        else:
            return f"Some error occured, the post doesn't belong to neither UserWall nor Fanpage"