from django.contrib import admin
from patient.models import PatientPrimaryData,FT,RP,PHR
# Register your models here.
admin.site.register(PatientPrimaryData)
# admin.site.register(PatientCount)
# admin.site.register(Appointment)
# admin.site.register(PatientVisit)
admin.site.register(FT)
admin.site.register(RP)
admin.site.register(PHR)