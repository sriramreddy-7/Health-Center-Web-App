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
    try:
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
    except:
        return HttpResponse('<h1 style="color:red;">Oops! This Patient is not yet compeleted the Initial Diagonisis At Junior Doctor</h1>')


def consultantDoctor_patientDiagonise_View_Edit(request,patient_id):
    pd=PatientPrimaryData.objects.get(patient_id=patient_id)
    # ad=FT.objects.get(patient_id=patient_id)
    # md=PHR.objects.get(patient=pd)
    context={
        'pd':pd,
        # 'ad':ad,
        # 'md':md,
    }
    return render(request,'consultantDoctor_patientDiagonise_View_Edit.html',context)


def consultantDoctor_precribeTest(request,appointment_id):
    if request.method == 'POST':
        x_ray = request.POST.get('x_ray')
        echocardiogram = request.POST.get('echocardiogram')
        electrocardiogram=request.POST.get('electrocardiogram')
        mri = request.POST.get('mri')
        stress_test=request.POST.get('stress_test')
        est=request.POST.get('est')
        blood_test=request.POST.get('blood_test')
        urine_test=request.POST.get('urine_test')
        ct_scan=request.POST.get('ct_scan')
        thread_mill_test = request.POST.get('thread_mill_test')
        echo=request.POST.get('echo')
        angiography=request.POST.get('angiography')
        print('X_Ray',x_ray)
        print('echocardiogram',echocardiogram)
        print('electrocardiogram',electrocardiogram)
        print('MRI Scan', mri)
        print('stress_test',stress_test)
        print('Blood Test',blood_test)
        print('Urine Test',urine_test)
        print('est',est)
        print('ct_scan',ct_scan)
        print('ECG',est)
        print('echo',echo)
        print('angiography',angiography)
        print('thread_mill_test ',thread_mill_test )
        return HttpResponse('<h1 style="color:green;">The Test Precribtion is Submitted to the Lab Incharge </h1>')
        
    ad=Visit.objects.get(appointment_id=appointment_id)
    pid=ad.patient_id
    pd=PatientPrimaryData.objects.get(patient_id=pid)
    context={
        'ad':ad,
        'pd':pd,
    }
    return render(request,'consultantDoctor_precribeTest.html',context)


def consultantDoctor_prescription(request):
    return render(request,'consultantDoctor_prescription.html')








