from django.db import models
from student.models import Student
from faculty.models import  Department, Semester
# Create your models here.

class FeeType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class feeStructure(models.Model):
    fee_type = models.ForeignKey(FeeType, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return str(self.fee_type) + " " + str(self.department) + " " + str(self.semester)

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100)
    payable = models.ForeignKey(FeeType, on_delete=models.CASCADE)
    req_amount = models.ForeignKey(feeStructure, on_delete=models.CASCADE)
    amount = models.IntegerField(blank=True, null=True)
    dues = models.IntegerField(blank=True, null=True)
    date = models.DateField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} {self.status} {self.date}"