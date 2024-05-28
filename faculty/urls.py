from django.urls import path

from . import views

app_name = 'faculty'

urlpatterns = [
    path('', views.index, name='Findex'),
    path('profile/', views.profile, name='profile'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('EditAttendance/', views.EditAttendance, name='EditAttendance'),
    path('notice/', views.notice, name='Addnotice'),
    path('sessionalMarks/', views.sessionalMarks, name='sessionalMarks'),
    path('updateschedule/', views.updateSchedule, name='updateSchedule'),
    path('editSubject/', views.editSubject, name='editSubject'),
    path('addSubject/<int:subId>', views.addSubject, name='addSubject'),
    path('addFaculty/<int:facId>', views.addFaculty, name='addFaculty'),
    path('editFaculty/', views.editFaculty, name='editFaculty'),
    path('deleteFaculty/<int:facId>', views.deleteFaculty, name='deleteFaculty'),
    path('deleteSubject/<int:subId>', views.deleteSubject, name='deleteSubject'),
    path('addStudent/', views.addStudent, name='addStudent'),
    path('createEmployee/', views.createEmployee, name='createEmployee'),
    path('createSubject/', views.createSubject, name='createSubject'),
    path('attendancwBySubject/<int:subId>', views.attendanceBySubject, name='attendanceBySubject'),
    path('viewNotice/', views.viewNotice, name='viewNotice'),
]