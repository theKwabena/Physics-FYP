from django.http import HttpResponse

from django.shortcuts import redirect
from django.core.exceptions import *
from portal.models import *


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
         if request.user.is_authenticated:
            return redirect ('Home')
         else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def registeredstudent(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.student.project is None:
            return redirect('Home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

def verificationRequired(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            request.user.student
            if request.user.is_authenticated and not request.user.student.verified:
                return redirect('verifyemail')
            else:
                return view_func(request, *args, **kwargs)  
        except Exception as e:
            if request.user.is_authenticated and not request.user.supervisor.verified:
                return redirect ('verifysupervisor')
            else:
                return view_func(request, *args, **kwargs)
    return wrapper_func


def approvalrequired(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.student.approved == False:
            return redirect('pending')
        elif request.user.student.approved == True:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                 return view_func(request, *args, **kwargs)
            else:
                return redirect('denied')
        return wrapper_func
    return decorator

# def projectRequired(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         if not Project.objects.filter(supervisor = request.user.supervisor).exists():
#             return redirect('Home')
#         else:
#             return view_func(request, *args, **kwargs)
#     return wrapper_func