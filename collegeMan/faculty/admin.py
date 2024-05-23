from django.contrib import admin
from .models import Semester, Subject, Schedule, Department, Employee ,Role, classTime, workingDays,Notice,SessionalMarks,sessional
# Register your models here.

admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Schedule)
admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Role)
admin.site.register(classTime)
admin.site.register(workingDays)
admin.site.register(Notice)
admin.site.register(SessionalMarks)
admin.site.register(sessional)
