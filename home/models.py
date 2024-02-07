from django.db import models

# Create your models here.

class OurStory(models.Model):
    title = models.CharField(max_length=200, help_text="Enter the page title")
    content = models.TextField(help_text="Enter the page content")
    image = models.ImageField(upload_to='our_story_images/', null=True, blank=True, help_text="Upload an image for the story")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title