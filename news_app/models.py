from django.db import models
from django.contrib.auth.models import User


class News(models.Model):
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=300)
    content = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    date_created = models.DateTimeField(
        auto_now_add=True
    )

    date_updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title