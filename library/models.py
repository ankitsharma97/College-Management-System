from django.db import models
from django.contrib.auth.models import User
from faculty.models import Semester, Department, Subject, Schedule, Employee, Role, classTime, workingDays,Notice,sessional,SessionalMarks
from student.models import Student
# Create your models here.

class Book(models.Model):
    bookId = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    
    user = models.ForeignKey(Student, on_delete=models.CASCADE,blank=True, null=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    isseued_date = models.DateField(blank=True, null=True) 
    submit_date = models.DateField(blank=True, null=True) 
    
    
    def __str__(self):
        return f"{self.title} ({self.author})"
    
    
    
class Fine(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    amount = models.IntegerField()
    fine_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.book} ({self.amount})"