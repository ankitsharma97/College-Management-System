from django.db import models
from faculty.models import Semester, Department, Subject, Schedule, Employee, Role, classTime, workingDays
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    abc_id = models.CharField(max_length=20, blank=True, null=True)
    registration_date = models.DateField(blank=True, null=True)
    
    STATUS_CHOICES = [
            ('Regular', 'Regular'),
            ('Lateral', 'Lateral'),
            ('Yearback', 'Yearback'),
            
        ]
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Regular')
    roll_no = models.CharField(max_length=20, blank=True, null=True)
    enrollment_no = models.CharField(max_length=20, blank=True, null=True)
    course = models.CharField(max_length=255,default='B.Tech')
    branch = models.ForeignKey(Department, on_delete=models.CASCADE,default=1)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,default=4)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    # personal details
    father_name = models.CharField(max_length=255, blank=True, null=True)
    mother_name = models.CharField(max_length=255, blank=True, null=True)
    father_mobile_no = models.CharField(max_length=15, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    adhar_no = models.CharField(max_length=20, blank=True, null=True)
    pan_no = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return self.name


class Attendance(models.Model):

    student = models.ForeignKey(Student, on_delete=models.CASCADE, blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    Semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True, null=True)
    deparment = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    classTime = models.ForeignKey(classTime, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.student.name + " " + self.subject.name + " " + str(self.date) + " " + str(self.classTime)