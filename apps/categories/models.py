from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField()

    @property
    def get_absolute_image_url(self):
        return f"{self.image.url}"

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
