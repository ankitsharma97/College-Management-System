# Generated by Django 4.2.13 on 2024-05-14 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0005_remove_schedule_end_time_remove_schedule_start_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='day',
            field=models.CharField(choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')], max_length=10),
        ),
    ]
