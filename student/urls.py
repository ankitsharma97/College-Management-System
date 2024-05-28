from django.urls import path

from . import views

app_name = 'student'

urlpatterns = [
    path('', views.Sindex, name='Sindex'),
    path('signUp/', views.signUp, name='signUp'),
    path('timeTable/', views.timeTable, name='timeTable'),
    path('attendance/', views.attendance, name='attendance'),
    path('marks/', views.marks, name='marks'),
    path('notice/', views.notice, name='notice'),
    path('profile/', views.profile, name='profile'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('message/', views.message, name='message'),
    path('createStudent/', views.createStudent, name='createStudent'),
    path('fee/', views.fee, name='fee'),
    path('yourBooks/', views.yourBooks, name='yourBooks'),
    path('yourSemesterBooks/', views.yourSemesterBooks, name='yourSemesterBooks'),
    path('searchBook/', views.searchBook, name='searchBook'),
    
]