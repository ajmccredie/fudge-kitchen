from django.db import models
from django.contrib.auth.models import User


class OurStory(models.Model):
    title = models.CharField(max_length=200, help_text="Enter the page title")
    content = models.TextField(
        max_length=1000, help_text="Enter the page content"
        )
    image = models.ImageField(
        null=True, blank=True,
        help_text="Upload an image for the story"
        )
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Inquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    email = models.EmailField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_new = models.BooleanField(default=True)
    is_dealt_with = models.BooleanField(default=False)

    def __str__(self):
        return f'Inquiry from {self.user.email} on {self.created_at}'
