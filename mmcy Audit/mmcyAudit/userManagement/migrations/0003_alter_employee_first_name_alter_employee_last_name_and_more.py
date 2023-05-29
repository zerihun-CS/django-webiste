# Generated by Django 4.1.6 on 2023-05-25 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0002_rename_department_employee_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='notes',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phone_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='private',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='status',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='timezone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='timezone_offset',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='username',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]