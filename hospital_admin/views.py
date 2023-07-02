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
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry


def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

@cache_control(no_cache=True, must_revalidate=True)
def logout_view(request):
    logout(request)
    response = HttpResponseRedirect('/')
    response.delete_cookie('sessionid')
    return response

def login_logs(request):
    user_logs = LogEntry.objects.filter(user__isnull=False).order_by('-action_time')[:10]
    return render(request, 'admin_login_logs.html', {'user_logs': user_logs})

