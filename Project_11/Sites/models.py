from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from django.db.models import Q
# Create your models here.

class UserWall(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wall")
    views = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s wall"
    

class Fanpage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fanpage")
    fanpage_name = models.CharField(max_length=150, unique=True)
    views = models.IntegerField(default=0)

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
        

class LastVisited(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="last_visited")
    last_visited = models.JSONField(default=list, blank=True)

    def update_last_visited(self, url):
        if url in self.last_visited:
            self.last_visited.remove(url)
        self.last_visited.insert(0, url)
        if len(self.last_visited) > 8:
            self.last_visited.pop()
        self.save()


class Friendship(models.Model):
    PENDING = "pending"
    ACCEPTED = "accepted"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted")
    ]

    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    last_action = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    class Meta:
        unique_together = ("sender", "receiver")

    def __str__(self):
        if self.status == self.ACCEPTED:
            return f"{self.sender.username} is a friend to {self.receiver.username}"
        else:
            return f"{self.sender.username} has sent an invitation to {self.receiver.username}"
    
    def update_last_action(self):
        self.last_action = timezone.now()
        self.save()

    @classmethod
    def get_friends(self, user):
        friendships = self.objects.filter(Q(sender=user, status=self.ACCEPTED) | Q(receiver=user, status=self.ACCEPTED))
        friends = []
        for friendship in friendships.order_by("-last_action"):
            friends.append(friendship.sender if friendship.receiver==user else friendship.receiver)
        return friends
    
    @classmethod
    def get_sent_invitations(self, user):
        friendships = self.objects.filter(sender=user, status=self.PENDING)
        sent_invitations = []
        for invitation in friendships.order_by("-last_action"):
            sent_invitations.append(invitation.receiver)
        return sent_invitations

    @classmethod
    def get_received_invitations(self, user):
        friendships = self.objects.filter(receiver=user, status=self.PENDING)
        received_invitations = []
        for invitation in friendships.order_by("-last_action"):
            received_invitations.append(invitation.sender)
        return received_invitations
    

class Message(models.Model):
    friendship = models.ForeignKey(Friendship, related_name="messages", on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} at {self.timestamp}"