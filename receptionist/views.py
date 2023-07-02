from django.shortcuts import render ,redirect
from django.contrib.auth import authenticate,logout,login
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import get_user_model
# from django.db.utils import IntegrityError
# from django.http import HttpResponse
# from django.contrib.auth import get_user_model
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from patient.models import PatientPrimaryData,FT
# Create your views here.


@login_required
def receptionist_dashboard(request):
    try:
        patient_count = PatientPrimaryData.objects.count()
        today= timezone.now().date()
        appointment_count = FT.objects.filter(appointment_date=today).count()
        return render(request,'receptionist_dashboard.html',{'patient_count':patient_count,'appointment_count':appointment_count})

    except:
        return HttpResponse("<h1> Please Login To Access this page</h1>")

@cache_control(no_cache=True, must_revalidate=True)
def logout_view(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.delete_cookie('sessionid')
    return response



def testing(request):
    return render(request ,'testing.html')


def newPatient_registration(request):
    if request.method =='POST':
        pname=request.POST.get('pname')
        pdob=request.POST['pdob']
        pgender=request.POST['pgender']
        page=request.POST['page']
        pgname=request.POST['pgname']
        pgrelation=request.POST['pgrelation']
        pmnum=request.POST['pmnum']
        pstate=request.POST['pstate']
        pdistrict=request.POST.get('pdistrict')
        address=request.POST.get('address')
        info=PatientPrimaryData(patient_name=pname,patient_dob=pdob,patient_gender=pgender,patient_age=page,guardian_name=pgname,relationship=pgrelation,mobile_number=pmnum,state=pstate,district=pdistrict,address=address)
        info.save()
        patient_id = info.patient_id
        return redirect('receptionist:patient_Acknowledgment', patient_id=patient_id)
    else:
        return render(request,'newPatient_registration.html')

def patient_Acknowledgment(request,patient_id):
    patient=PatientPrimaryData.objects.get(patient_id=patient_id)
    current_time = timezone.now()
    flag=patient.patient_id
    flag=flag[-4:]
    return render(request, 'patient_Acknowledgment.html', {'patient': patient, 'current_time':current_time,'flag':flag})

# def oldPatient_registration(request):
#     return render(request,'oldPatient_registration.html')

# def patient_details(request):
#     if request.method =='POST':
#         patient_id = request.GET.get('patient_id')
#         patient = None
#         if patient_id:
#             try:
#                 patient = PatientPrimaryData.objects.get(patient_id=patient_id)
#             except PatientPrimaryData.DoesNotExist:
#                 pass
#         return render(request,'oldPatient_registration.html',{'patient': patient, 'patient_id': patient_id})
#     else:
#         return HttpResponse("<h1>Invalid Request</h2>")

def oldPatient_registration(request):
    if request.method =='GET':
        patient_id = request.GET.get('patient_id')
        patient = None
        if patient_id:
            try:
                patient = PatientPrimaryData.objects.get(patient_id=patient_id)
            except PatientPrimaryData.DoesNotExist:
                pass
        return render(request, 'oldPatient_registration.html', {'patient': patient, 'patient_id': patient_id})
    else:
        return render(request, 'oldPatient_registration.html')


def appointment(request,patient_id):
    patient=PatientPrimaryData.objects.get(patient_id=patient_id)
    pid=patient.patient_id
    info=FT(patient_id=pid)
    info.save()
    flag=FT.objects.get(patient_id=patient_id)
    return render(request,'appointment.html',{'patient':patient,'flag':flag})

def receptionist_patientList(request):
    patient=PatientPrimaryData.objects.all()
    patient_count = PatientPrimaryData.objects.count()
    return render(request,'receptionist_patientList.html',{'patient':patient,'patient_count':patient_count})

def receptionist_appointmentList(request):
    apd=FT.objects.all()
    return render(request,'receptionist_appointmentList.html',{'apd':apd})


def receptionist_patient_View_Edit(request,patient_id):
    patient=PatientPrimaryData.objects.get(patient_id=patient_id)
    # apd=FT.objects.get(patient_id=patient_id)
    context={
            'patient':patient,
    }
    return render(request,'receptionist_patient_View_Edit.html',context)



def receptionist_patientSearch(request):
    if request.method =='GET':
        search_query = request.GET.get('search_query')
        search_type  = request.GET.get('search_type')
        patients = None
        if search_query:
            try:
                if search_type == 'patient_id':
                    patients = PatientPrimaryData.objects.filter(patient_id=search_query)
                elif search_type == 'mobile_number':
                    patients = PatientPrimaryData.objects.filter(mobile_number=search_query)
                elif search_type == 'fname':
                    patients = PatientPrimaryData.objects.filter(patient_name__icontains=search_query)
                else:
                    patients = None
                # patient = PatientPrimaryData.objects.get(patient_id=patient_id)
            except PatientPrimaryData.DoesNotExist:
                pass
        return render(request, 'receptionist_patientSearch.html', {'patients': patients, 'search_query': search_query })
    else:
        return render(request, 'receptionist_patientSearch.html')

