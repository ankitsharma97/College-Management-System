# Generated by Django 4.2.13 on 2024-05-15 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('faculty', '0011_alter_subject_subject_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('erp_id', models.CharField(blank=True, max_length=20, null=True)),
                ('registration_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Regular', 'Regular'), ('Lateral', 'Lateral'), ('Yearback', 'Yearback')], default='Regular', max_length=50)),
                ('roll_no', models.CharField(blank=True, max_length=20, null=True)),
                ('enrollment_no', models.CharField(blank=True, max_length=20, null=True)),
                ('course', models.CharField(default='B.Tech', max_length=255)),
                ('branch', models.CharField(choices=[('IT', 'Information Technology'), ('ME', 'Mechanical Engineering'), ('CE', 'Civil Engineering')], default=1, max_length=50)),
                ('semester', models.CharField(choices=[('1', '1st Semester'), ('2', '2nd Semester'), ('3', '3rd Semester'), ('4', '4th Semester'), ('5', '5th Semester'), ('6', '6th Semester'), ('7', '7th Semester'), ('8', '8th Semester')], default=4, max_length=10)),
                ('mobile_no', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.BooleanField(default=False)),
                ('Semester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty.semester')),
                ('deparment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty.department')),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='faculty.subject')),
            ],
        ),
    ]