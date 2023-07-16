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
from patient.models import PatientPrimaryData,FT,RP,Test,Visit
from django.db.models import Q
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

def lab_incharge_upload_report(request,appointment_id):
    print(appointment_id)
    appid=Visit.objects.get(appointment_id=appointment_id)
    apd=appid.patient_id
    patient=PatientPrimaryData.objects.get(patient_id=apd)
    context={
        'appid':appid,
        'patient':patient,
    }
    if request.method=='POST':
        patient_id = request.POST['patient_id']
        report_file = request.FILES['report_file']
        rp = RP(patient_id=patient_id, report_file=report_file)
        rp.save()
        patient=RP.objects.all()
        return render(request,'lab_Incharge_patient_reports.html',{'patient':patient})
    else:
        return render(request,'lab_incharge_upload_report.html',context)


def lab_Incharge_patient_reports(request):
    patient=RP.objects.all()
    return render(request,'lab_Incharge_patient_reports.html',{'patient':patient})

def lab_Incharge_patient_reports_gallery(request):
    patient=RP.objects.all()
    return render(request,'lab_Incharge_patient_reports_gallery.html',{'patient':patient})


def lab_incharge_test_orders(request):
    patient=Test.objects.exclude(
    Q(test1__isnull=True) &
    Q(test2__isnull=True) &
    Q(test3__isnull=True) &
    Q(test4__isnull=True) &
    Q(test5__isnull=True) &
    Q(test6__isnull=True) &
    Q(test7__isnull=True) &
    Q(test8__isnull=True) &
    Q(test9__isnull=True) &
    Q(test10__isnull=True) &
    Q(test11__isnull=True) &
    Q(test12__isnull=True) &
    Q(test13__isnull=True) &
    Q(test14__isnull=True) &
    Q(test15__isnull=True) &
    Q(test16__isnull=True) &
    Q(test17__isnull=True) &
    Q(test18__isnull=True)
    )
    return render(request,'lab_incharge_test_orders.html',{'patient':patient})