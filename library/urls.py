from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.Lindex, name='Lindex'),
    path('addBook/<int:bookId>', views.addBook, name='addBook'),
    path('search/', views.search, name='search'),
    path('viewBook/', views.viewBook, name='viewBook'),
    path('profile/', views.profile, name='profile'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('viewFine/', views.viewFine, name='viewFine'),
    path('deleteBook/<int:bookId>', views.deleteBook, name='deleteBook'),
    path('viewFine/', views.viewFine, name='viewFine'),
    path('addFine/', views.addFine, name='addFine'),
    path('addnotice/', views.notice, name='notice'),
    path('issueBook/', views.issueBook, name='issueBook'),
    path('submitBook/', views.submitBook, name='submitBook'),
    path('viewNotice/', views.viewNotice, name='viewNotice'),
]