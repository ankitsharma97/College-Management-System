# Generated by Django 4.2.13 on 2024-05-15 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faculty', '0011_alter_subject_subject_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='classTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.CharField(max_length=50)),
                ('end_time', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='workingDays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='schedule',
            name='time',
            field=models.CharField(choices=[('09:30', '09:30 - 10:20'), ('10:20', '10:20 - 11:10'), ('11:10', '11:10 - 12:00'), ('12:00', '12:00 - 12:50'), ('12:50', '12:50 - 02:20'), ('02:20', '02:20 - 04:00'), ('04:00', '04:00 - 05:00')], max_length=50),
        ),
    ]
