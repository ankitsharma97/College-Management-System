# Generated by Django 4.2.13 on 2024-05-15 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0010_subject_subject_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='subject_Type',
            field=models.CharField(choices=[('Theory', 'Theory'), ('Practical', 'Practical')], default='Theory', max_length=50),
        ),
    ]
