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
from patient.models import PatientPrimaryData,FT,RP
# Create your views here.

def lab_incharge_dashboard(request):
    return render(request,'lab_incharge_dashboard.html')

@cache_control(no_cache=True, must_revalidate=True)
def logout_view(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.delete_cookie('sessionid')
    return response


def lab_incharge_patient_wise_report(request):
    patient=PatientPrimaryData.objects.all()
    context={
    'patient':patient,
    }
    return render(request,'lab_incharge_PWR.html',context)

def lab_incharge_upload_report(request,patient_id):
    patient=PatientPrimaryData.objects.get(patient_id=patient_id)
    if request.method=='POST':
        patient_id = request.POST['patient_id']
        report_file = request.FILES['report_file']
        rp = RP(patient_id=patient_id, report_file=report_file)
        rp.save()
        patient=RP.objects.all()
        return render(request,'lab_Incharge_patient_reports.html',{'patient':patient})
    else:
        return render(request,'lab_incharge_upload_report.html',{'patient':patient})


def lab_Incharge_patient_reports(request):
    patient=RP.objects.all()
    return render(request,'lab_Incharge_patient_reports.html',{'patient':patient})

def lab_Incharge_patient_reports_gallery(request):
    patient=RP.objects.all()
    return render(request,'lab_Incharge_patient_reports_gallery.html',{'patient':patient})


