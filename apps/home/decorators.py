from django.http import HttpResponse

from django.shortcuts import redirect


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
            return redirect('projects')
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