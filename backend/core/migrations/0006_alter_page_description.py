# Generated by Django 4.0.4 on 2022-04-27 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_page_description_page_headline_h1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='description',
            field=models.TextField(max_length=255, verbose_name='Тег description'),
        ),
    ]
