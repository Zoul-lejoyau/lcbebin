from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    class Meta:
        ordering = ('slug',)
    
    def __str__(self):
        return f'{self.id}: {self.name}'
    
    def get_absolute_url(self):
        return f'/{self.slug}/'



class Formation(models.Model):
    category = models.ForeignKey(Category, related_name='formations', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    duration = models.DurationField(default='3')
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('-date',)
  
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.thumbnail.path)

        if img.height > 200 or img.width > 300:
            output_size = (300, 200)
            img.thumbnail(output_size)
            img.save(self.thumbnail.path)
    