import os
import random
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.categories.models import Category

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='posts'
    )
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft'
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

class PostImage(models.Model):
    image = models.ImageField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images'
    )
    @property
    def get_absolute_image_url(self):
        return f"{self.image.url}"

    def __str__(self):
        return f'{self.post.title}.jpg'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user_name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user_name, self.post)
