from django.contrib import admin
from patient.models import PatientPrimaryData,FT,RP,PHR,Visit
# Register your models here.
admin.site.register(PatientPrimaryData)
# admin.site.register(PatientCount)
# admin.site.register(Appointment)
admin.site.register(Visit)
admin.site.register(FT)
admin.site.register(RP)
admin.site.register(PHR)