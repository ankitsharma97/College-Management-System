from django.contrib import admin
from .models import Student
from .models import Attendance

admin.site.register(Student)
admin.site.register(Attendance)

