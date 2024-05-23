# Generated by Django 4.2.13 on 2024-05-15 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0011_alter_subject_subject_type'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.department'),
        ),
        migrations.AlterField(
            model_name='student',
            name='semester',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.semester'),
        ),
    ]