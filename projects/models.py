from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from ckeditor_uploader.fields import RichTextUploadingField

class Project(models.Model):
    title = models.CharField(max_length=200)

    slug = models.SlugField(unique=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

    title_link = models.TextField(blank=True)
    hidden = models.BooleanField(default=False)

    description = RichTextUploadingField(blank=True)
    image = models.ImageField(upload_to='projects/')
    link = models.ManyToManyField('Link', related_name='projects', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Link(models.Model):
    url = models.URLField()
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.url