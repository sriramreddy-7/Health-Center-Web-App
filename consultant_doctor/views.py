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
from patient.models import PatientPrimaryData,FT,PHR,Visit,JDD


def consultantDoctor_dashboard(request):
    patient_count=PatientPrimaryData.objects.count()
    appt_count=Visit.objects.count()
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
    patient=Visit.objects.all()
    return render(request,'consultantDoctor_appointmentList.html',{'patient':patient})


def consultantDoctor_patientDiagonise(request,appointment_id):
    ad=Visit.objects.get(appointment_id=appointment_id)
    pid=ad.patient_id
    pd=PatientPrimaryData.objects.get(patient_id=pid)
    phr=JDD.objects.get(appointment_id=appointment_id)
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


def consultantDoctor_precribeTest(request):
    if request.method == 'POST':
        selected_tests = []
        for i in range(len(request.POST.getlist('test-id-0'))):
            test_id = request.POST.get(f'test-id-{i}')
            test_name = request.POST.get(f'test-name-{i}')
            selected_tests.append({'id': test_id, 'name': test_name})
            print('Test_id',test_id)
            print('Test_Name',test_name)
            print('Selected Tests',selected_tests)
        # test_ids = request.POST.getlist('test-id')
        # test_names = request.POST.getlist('test-name')
        # blood_test=request.POST.get('blood_test')
        # urine_test=request.POST.get('urine_test')
        # x_ray=request.POST.get('x_ray')
        # mri_scan=request.POST.get('mri_scan')
        # ecg=request.POST.get('ecg')
        # for test_id, test_name in zip(test_ids, test_names):
        #     print("Test ID:", test_id)
        #     print("Test Name:", test_name)
        # print('Blood Test',blood_test)
        # print('Urine Test',urine_test)
        # print('X_Ray',x_ray)
        # print('MRI Scan',mri_scan)
        # print('ECG',ecg)
        # print('Test_ID',test_ids)
        # print('Test_Name',test_names)
    return render(request,'consultantDoctor_precribeTest.html')












