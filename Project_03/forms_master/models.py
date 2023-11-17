from django.db import models

class FormsModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(default = "No description available")
    last_modified = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title