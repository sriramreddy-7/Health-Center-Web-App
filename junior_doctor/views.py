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
# Create your views here.
from datetime import datetime

def juniorDoctor_dashboard(request):
    return render(request,'juniorDoctor_dashboard.html')

def juniorDoctor_appointmentList(request):
    patient=FT.objects.all()
    return render(request,'juniorDoctor_appointmentList.html',{'patient':patient})

def page_not_found(request):
    return render(request,'page_not_found.html')

def juniorDoctor_patientList(request):
    patient=PatientPrimaryData.objects.all()
    patient_count=PatientPrimaryData.objects.count()
    return render(request,'juniorDoctor_patientList.html',{'patient':patient,'patient_count':patient_count})


def juniorDoctor_appointmentList_FilterbyDate(request):
    patient=FT.objects.all()
    now= datetime.now()
    return render(request,'juniorDoctor_appointmentList_FilterbyDate.html',{'patient':patient,'now':now })

@cache_control(no_cache=True, must_revalidate=True)
def logout_view(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.delete_cookie('sessionid')
    return response

def juniorDoctor_patientDiagonise(request,patient_id):
    pd=PatientPrimaryData.objects.get(patient_id=patient_id)
    ad=FT.objects.get(patient_id=patient_id)
    context={
        'pd':pd,
        'ad':ad
    }
    if request.method == 'POST':
        height = request.POST['height']
        weight = request.POST['weight']
        pulse = request.POST['pulse']
        bp = request.POST['bp']
        is_diabetic = 'is_diabetic' in request.POST
        diabetic_level = request.POST['diabetic_level'] if is_diabetic else None
        phi = request.POST['phi']
        pov = request.POST['pov']
        remarks = request.POST['remarks']
        health_record = PHR.objects.create(
            patient=pd,
            height=height,
            weight=weight,
            pulse=pulse,
            bp=bp,
            is_diabetic=is_diabetic,
            diabetic_level=diabetic_level,
            phi=phi,
            pov=pov,
            remarks=remarks
        )
        health_record.save()
        return redirect('junior_doctor:juniorDoctor_appointmentList')
    return render(request,'juniorDoctor_patientDiagonise.html',context)


def juniorDoctor_patientDiagonise_View_Edit(request,patient_id):
    pd=PatientPrimaryData.objects.get(patient_id=patient_id)
    ad=FT.objects.get(patient_id=patient_id)
    md=PHR.objects.get(patient=pd)
    context={
        'pd':pd,
        'ad':ad,
        'md':md,
    }
    return render(request,'juniorDoctor_patientDiagonise_View_Edit.html',context)
    # else:
    #     return render(request,'page_not_found.html')
    # return render(request,'juniorDoctor_patientDiagonise_View_Edit.html',context)
