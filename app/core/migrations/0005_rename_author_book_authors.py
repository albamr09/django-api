# Generated by Django 3.2.7 on 2021-09-28 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='author',
            new_name='authors',
        ),
    ]