# Generated by Django 4.2.13 on 2024-05-16 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0016_sessionalmarks_dept_sessionalmarks_sem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sessionalmarks',
            old_name='sessional',
            new_name='sessionalno',
        ),
        migrations.AlterField(
            model_name='sessionalmarks',
            name='marks',
            field=models.IntegerField(default=0),
        ),
    ]
