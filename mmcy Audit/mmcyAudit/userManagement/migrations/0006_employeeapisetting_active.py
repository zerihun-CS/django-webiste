# Generated by Django 4.1.6 on 2023-05-28 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0005_employeeapisetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeeapisetting',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]