from django.contrib import admin
from .models import Book, Fine
# Register your models here.

admin.site.register(Book)
admin.site.register(Fine)