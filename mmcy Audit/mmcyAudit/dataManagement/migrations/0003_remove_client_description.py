# Generated by Django 4.1.6 on 2023-05-23 15:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataManagement', '0002_rename_onenote_link_client_website_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='description',
        ),
    ]
