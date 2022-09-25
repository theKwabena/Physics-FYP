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
            return redirect('Home')
        else:
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


def incompleteRegistration(view_func):
    def wrapper_func(request, *args, **kwargs):
        try:
            request.user.supervisor
            if request.user.supervisor.rank is None or request.user.supervisor.role is None:
                return redirect('regStep2')
            else:
                return view_func(request, *args, **kwargs)
        except Exception as e:
            print(e)
            return redirect('regStep2')
    return wrapper_func


