from django.db import models
from django.utils.text import slugify
from unidecode import unidecode

class Project(models.Model):
    title = models.CharField(max_length=200)
    
    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    description = models.TextField()
    image = models.ImageField(upload_to='projects/upload_media')
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
