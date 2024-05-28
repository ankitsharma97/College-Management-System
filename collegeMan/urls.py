from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student/', include(('student.urls', 'student'), namespace='student')),
    path('faculty/', include(('faculty.urls', 'faculty'), namespace='faculty')),
    path('library/', include(('library.urls', 'library'), namespace='library')),
    path('feeMan/', include(('feeMan.urls', 'feeMan'), namespace='feeMan')),
    path('', include(('main.urls', 'main'), namespace='main')),
]
