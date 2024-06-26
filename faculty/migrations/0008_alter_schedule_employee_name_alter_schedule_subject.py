# Generated by Django 4.2.13 on 2024-05-14 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0007_alter_schedule_lecture_number_alter_schedule_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='employee_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty.employee'),
        ),
        migrations.AlterField(
            model_name='schedule',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty.subject'),
        ),
    ]
