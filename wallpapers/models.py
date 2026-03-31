from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    icon_class = models.CharField(max_length=50, default="bi-image")

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Wallpaper(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='wallpapers/', null=True, blank=True)
    image_url = models.URLField(max_length=1000, null=True, blank=True)
    hd_url = models.URLField(max_length=1000, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='wallpapers')
    is_featured = models.BooleanField(default=False)
    favorites = models.ManyToManyField(User, related_name='fav_wallpapers', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @property
    def get_display_url(self):
        if self.image:
            return self.image.url
        return self.image_url
