# Generated by Django 4.2.4 on 2023-09-04 19:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("phone_books", "0003_alter_phonebook_tel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="phonebook",
            name="image",
            field=models.ImageField(
                upload_to="phone_book_image", verbose_name="Kapak Fotografı"
            ),
        ),
    ]
