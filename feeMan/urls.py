from django.urls import path

from . import views

app_name = 'feeMan'

urlpatterns = [
    path('', views.Aindex, name='Aindex'),
    path('profile/', views.profile, name='profile'),
    path('editProfile/', views.editProfile, name='editProfile'),
    path('addnotice/', views.notice, name='notice'),
    path('addFee/<int:fee_id>/', views.addFee, name='addFee'), 
    path('viewFee/', views.viewFee, name='viewFee'),
    path('searchFee/', views.searchFee, name='searchFee'),
    path('viewNotice/', views.viewNotice, name='viewNotice'),

]