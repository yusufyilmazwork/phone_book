from django.contrib import admin
from django.db import models
from phone_books.models import PhoneBook, Category

# Register your models here.

class PhoneBookAdmin(admin.ModelAdmin):
    list_display = ['ad', 'soyad', 'tel', 'email']
    search_fields = ["ad", "soyad", "tel", "email", "adres", "category",]
    list_filter = ("category")

admin.site.register(PhoneBook)
admin.site.register(Category)