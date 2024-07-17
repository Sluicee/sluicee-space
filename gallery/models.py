from django.db import models
from django.utils.text import slugify
from unidecode import unidecode
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
import os
from django.core.files.base import ContentFile
    
class Album(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Camera(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    lens = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.brand} {self.model} {self.lens}"
    
class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='photos/')
    thumbnail = models.ImageField(upload_to='photos/thumbnails/', editable=False, blank=True, null=True)
    description = models.TextField(blank=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, related_name='photos')
    camera = models.ForeignKey(Camera, related_name='photos', on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.thumbnail:
            self.create_thumbnail()

    def create_thumbnail(self):
        image_path = self.image.path
        image = Image.open(image_path)

        # Определяем размер миниатюры с сохранением пропорций
        max_size = (300, 500)  # Максимальный размер миниатюры
        image.thumbnail(max_size, Image.LANCZOS)

        # Сохраняем миниатюру
        thumbnail_dir = os.path.join(os.path.dirname(image_path), 'thumbnails')
        if not os.path.exists(thumbnail_dir):
            os.makedirs(thumbnail_dir)

        # Генерируем уникальное имя для миниатюры
        thumbnail_filename = f"thumbnail_{self.pk}.jpg"  # Пример уникального имени
        thumbnail_path = os.path.join(thumbnail_dir, thumbnail_filename)
        image.save(thumbnail_path, format='JPEG')

        # Открываем файл миниатюры и сохраняем его в поле thumbnail модели
        with open(thumbnail_path, 'rb') as f:
            thumbnail_content = f.read()
            self.thumbnail.save(thumbnail_filename, ContentFile(thumbnail_content), save=False)

        # Сохраняем изменения в модели
        self.save(update_fields=['thumbnail'])

    def __str__(self):
        return self.title