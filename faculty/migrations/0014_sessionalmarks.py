# Generated by Django 4.2.13 on 2024-05-16 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_rename_class_time_attendance_classtime'),
        ('faculty', '0013_notice'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionalMarks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sessional', models.CharField(choices=[('Sessional1', 'Sessional1'), ('Sessional2', 'Sessional2')], max_length=50)),
                ('marks', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.employee')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='faculty.subject')),
            ],
        ),
    ]