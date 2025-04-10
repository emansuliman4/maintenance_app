from django.contrib import admin
from .models import Call, Reception, ReceptionPhoto, RepairNote
# Register your models here.

admin.site.register(Call)
admin.site.register(Reception)
admin.site.register(ReceptionPhoto)
admin.site.register(RepairNote)
