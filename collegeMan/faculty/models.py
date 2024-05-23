from django.db import models
from django.contrib.auth.models import User

class Semester(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class classTime(models.Model):
    start_time = models.CharField(max_length=50)
    end_time = models.CharField(max_length=50)
    
    def __str__(self):  
        return f"{self.start_time} - {self.end_time}"
    
class workingDays(models.Model):
    day = models.CharField(max_length=50)
    
    def __str__(self):
        return self.day

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True, null=True)
    name = models.CharField(max_length=100)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    role = models.ForeignKey('Role', on_delete=models.CASCADE,default=1)
    joining_date = models.DateField(blank=True, null=True)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    mother_name = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    def __str__(self):
        return f"{self.name} ({self.department})"

class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Subject(models.Model):
    
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    branch = models.ForeignKey(Department, on_delete=models.CASCADE,default=1)
    employee_name = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    sub_choice = [
        ('Theory', 'Theory'),
        ('Practical', 'Practical'),
    ]
    subject_Type = models.CharField(max_length=50,choices=sub_choice, default='Theory')

    def __str__(self):
        return f"{self.code} - {self.name} (Semester: {self.semester})"

class Schedule(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    day = models.ForeignKey(workingDays, on_delete=models.CASCADE,blank=True, null=True)
    lecture_number = models.CharField(max_length=3,blank=True, null=True)
    time = models.ForeignKey(classTime, on_delete=models.CASCADE,blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,blank=True, null=True)
    employee_name = models.ForeignKey(Employee, on_delete=models.CASCADE,blank=True, null=True)

    def __str__(self):
        return f"{self.day} - {self.subject} - {self.employee_name}"

class Notice(models.Model):
    Title = models.CharField(max_length=100)
    Description = models.TextField()
    date = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Department, on_delete=models.CASCADE)
    by = models.ForeignKey(Employee, on_delete=models.CASCADE)
    who = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.Title
 
class sessional(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
       
class SessionalMarks(models.Model):
    sem = models.ForeignKey(Semester, on_delete=models.CASCADE,default=1)
    dept = models.ForeignKey(Department, on_delete=models.CASCADE,default=1)
    student = models.ForeignKey('student.Student', on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Employee, on_delete=models.CASCADE)
    sessionalno = models.ForeignKey(sessional, on_delete=models.CASCADE)
    marks = models.IntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student} - {self.subject} - {self.sessionalno} - {self.marks}"