import os, sys
from PIL import Image
from io import BytesIO
from random import randint
from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from apps.categories.models import Category


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    print('base_name', base_name)
    name, ext = os.path.splitext(base_name)
    print(name, ext)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = randint(1, 3999999999)
    print('newfilename', new_filename)
    name, ext = get_filename_ext(filename)
    print(name, ext)
    final_filename = f'{new_filename}{ext}'
    print('final_filename', final_filename)
    return f'post_images/{new_filename}/{final_filename}'


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
    category = models.ManyToManyField(Category, related_name='categories')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft'
    )

    class Meta:
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class PostImage(models.Model):
    image = models.ImageField(upload_to=upload_image_path)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='images'
    )
    @property
    def get_absolute_image_url(self):
        return f"{self.image.url}"

    def compressImage(self, image):
        imageTemproary = Image.open(image)
        outputIoStream = BytesIO()
        imageTemproaryResized = imageTemproary.resize((1020, 573))
        imageTemproary.save(outputIoStream, format='JPEG', quality=50)
        outputIoStream.seek(0)
        image = InMemoryUploadedFile(
            outputIoStream, 'ImageField', '%s.jpg' % image.name.split('.')[0],
            'image/jpeg', sys.getsizeof(outputIoStream), None
        )
        return image

    def save(self, *args, **kwargs):
        if not self.id:
            self.image = self.compressImage(self.image)
        super(PostImage, self).save(*args, **kwargs)

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
