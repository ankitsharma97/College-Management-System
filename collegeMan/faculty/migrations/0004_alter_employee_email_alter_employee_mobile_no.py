# Generated by Django 4.2.13 on 2024-05-14 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0003_remove_schedule_employee_code_employee_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='mobile_no',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
