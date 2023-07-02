from django.shortcuts import render,get_object_or_404

from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,logout,login
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_control
from django.http import HttpResponseRedirect
from patient.models import PatientPrimaryData,FT,PHR


def consultantDoctor_dashboard(request):
    patient_count=PatientPrimaryData.objects.count()
    appt_count=FT.objects.count()
    common_records = PatientPrimaryData.objects.filter(patient_id__in=FT.objects.values('patient_id'))
    data={
        'patient_count':patient_count,
        'appt_count':appt_count,
        'common_records':common_records,
    }
    return render(request,'consultantDoctor_dashboard.html',data)

@cache_control(no_cache=True, must_revalidate=True)
def logout_view(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.delete_cookie('sessionid')
    return response

def consultantDoctor_patientList(request):
    patient=PatientPrimaryData.objects.all()
    return render(request,'consultantDoctor_patientList.html',{'patient':patient})

def consultantDoctor_appointmentList(request):
    patient=FT.objects.all()
    return render(request,'consultantDoctor_appointmentList.html',{'patient':patient})


def consultantDoctor_patientDiagonise(request,patient_id):
    pd=PatientPrimaryData.objects.get(patient_id=patient_id)
    ad=FT.objects.get(patient_id=patient_id)
    phr=PHR.objects.get(patient=pd)
    context={
        'pd':pd,
        'ad':ad,
        'phr':phr,
    }
    return render(request,'consultantDoctor_patientDiagonise.html',context)


def consultantDoctor_patientDiagonise_View_Edit(request,patient_id):
    pd=PatientPrimaryData.objects.get(patient_id=patient_id)
    ad=FT.objects.get(patient_id=patient_id)
    md=PHR.objects.get(patient=pd)
    context={
        'pd':pd,
        'ad':ad,
        'md':md,
    }
    return render(request,'consultantDoctor_patientDiagonise_View_Edit.html',context)















