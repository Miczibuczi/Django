from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image

class Post(models.Model):
    image = models.ImageField(default="default_foo.png", upload_to="")
    caption = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author.username}\'s Post - {self.caption}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 400 or img.width > 400:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Comment(models.Model):
	post = models.ForeignKey("Post", on_delete=models.CASCADE, related_name="comments")
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "comment on {} by {}".format(self.post.title,self.user.username)