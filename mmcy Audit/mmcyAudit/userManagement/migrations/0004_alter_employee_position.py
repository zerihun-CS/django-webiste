# Generated by Django 4.1.6 on 2023-05-25 17:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userManagement', '0003_alter_employee_first_name_alter_employee_last_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='userManagement.position'),
        ),
    ]