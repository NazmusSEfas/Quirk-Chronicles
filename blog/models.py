from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
#the main blog post
class Post(models.Model):
    title = models.CharField(max_length=200)
    summery = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    published_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)  # Add created_by field
    

    def publish(self):
        self.published_at = timezone.now()
        self.save()

    def __str__(self):
        return self.title
    
# Paragraph model linked to a Post
class Paragraph(models.Model):
    post = models.ForeignKey(Post, related_name='paragraphs', on_delete=models.CASCADE)
    content = models.TextField()
    order = models.PositiveIntegerField(default=0)  # To order paragraphs within a post
    

    def __str__(self):
        return f"Paragraph {self.order} for {self.post.title}"


# Image model linked to a Paragraph (optional)
class Image(models.Model):
    paragraph = models.ForeignKey(Paragraph, related_name='images', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='paragraph_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for Paragraph {self.paragraph.order} in {self.paragraph.post.title}"