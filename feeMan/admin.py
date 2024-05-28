from django.contrib import admin
from .models import FeeType, feeStructure, Fee
admin.site.register(FeeType)
admin.site.register(feeStructure)
admin.site.register(Fee)
# Register your models here.
