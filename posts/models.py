from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    liked = models.ManyToManyField(User, related_name="liked")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"post {self.id}"
