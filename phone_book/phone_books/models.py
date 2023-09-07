from django.db import models
from django.utils.text import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}"
    
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"


class PhoneBook(models.Model):
    ad = models.CharField(max_length=200)
    soyad = models.CharField(max_length=200)
    tel = models.CharField(max_length=11)
    email = models.EmailField(max_length=250, blank=True, null=True)
    image = models.ImageField(upload_to="phone_book_image", verbose_name="Kapak Fotografı")
    adres = models.TextField(max_length=500, blank=True, null=True)
    category = models.ManyToManyField(Category, related_name="phone_books")
    slug = models.SlugField(max_length=270, unique=True, editable=False)

    def __str__(self):
        return f"{self.ad} {self.soyad}"
    
    class Meta:
        verbose_name = "Kişi"
        verbose_name_plural = "Kişiler"


    def save(self, *args, **kwargs):
        self.slug = slugify(self.ad)
        super().save(*args,**kwargs)


