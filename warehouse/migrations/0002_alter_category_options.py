# Generated by Django 5.1.2 on 2024-10-13 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'category', 'verbose_name_plural': 'categories'},
        ),
    ]
