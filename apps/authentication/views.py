
# Create your views here.
import time

from django.contrib import messages
import pandas as pd
import json
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm, SupervisorEmailVerificationForm, PasswordChangingForm, UserExistForm, NoEmailForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.http import HttpResponse, HttpResponseRedirect
from .utils import generate_supervisor_token
from django.urls import reverse_lazy
from .cusfunctions import generate_username
from django.template.loader import render_to_string
from notifications.tasks import send_verification_email
from django.utils.decorators import method_decorator
from coordinator.decorators import verificationRequired
from .decorators import noUser, incompleteRegistration



from portal.models import Student, Supervisor,  studentData

@unauthenticated_user
def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                if user.groups.filter(name = 'Coordinator'):
                    return redirect('coordinator')
                elif user.groups.filter(name = 'Supervisor'):
                    try:
                        request.GET['next']
                        url = request.GET['next']
                        return redirect(url)
                    except Exception as e:   
                        return redirect('supervisor')
                
                if user.groups.filter(name = 'Student'):
                    try:
                        if 'projects' in request.GET['next']:
                            url = request.GET['next'].removesuffix('/register')
                            return redirect(url + '/details')
                        elif request.GET['next']:
                            url = request.GET['next']
                            return redirect(url)
                    except Exception as e:
                        if user.student.project is None:
                            return redirect('projects')
                        else:
                            return redirect('studentview')
                else:   
                    return redirect('regStep2')
                if not user.groups.filter(name = 'Coordinator') and not user.groups.filter(name = 'Supervisor') and not user.groups.filter(name = 'Student'):
                    return redirect('regStep2')
            else:
                msg = 'Check username and password and try again'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})




@unauthenticated_user
def register_user(request):
    msg = None
    form = SignUpForm(request.POST or None)
    if request.method == "POST":
        if request.POST.get('key') == 'physicsProject':
            if form.is_valid():
                first_name = form.cleaned_data['first_name']
                other_names = form.cleaned_data['last_name']
                generated_username = generate_username(first_name, other_names)
                user = form.save(commit = False)
                user.username = generated_username
                user.save()
                login(request,  user = authenticate(request, username =generated_username, password = form.cleaned_data['password1']))
                return redirect('regStep2')
            # else:
            #  msg = 'Form is not valid'
        else:
            form = SignUpForm(request.POST or None)
            msg = 'Invalid login key, check your login key and try again'
    context = {
        'form': form,
        'message': msg
    }
    return render(request, 'accounts/register.html', context)


@noUser
def registerStep2(request):
    user = request.user
    if request.method == "POST":
        if request.POST.get('role') == 'Supervisor':
            title = request.POST.get('title')
            # print(rank)
            role = request.POST.get('role')
            group, created = Group.objects.get_or_create(name = 'Supervisor')
            # group = Group.objects.get_or_create(name = 'Supervisor')
            user.groups.add(group)
            Supervisor.objects.create(user = request.user, email = request.user.email, rank = title, role = role, first_name = request.user.first_name, other_names = request.user.last_name)
            return redirect('regStep3')
        
        
        elif request.POST.get('role') == 'Project Coordinator':
            title = request.POST.get('title')
            print(title)
            role = request.POST.get('role')
            group, created = Group.objects.get_or_create(name = 'Coordinator')
            user.groups.add(group)
            Supervisor.objects.create(user = request.user, email = request.user.email, rank = title, role = role, first_name = request.user.first_name, other_names = request.user.last_name )
            return redirect('regStep3')
        
       # login(request,  user = authenticate(request, username =form.cleaned_data['username'], password = form.cleaned_data['password1']))
    return render(request, 'accounts/regis2.html')

@incompleteRegistration
def sendVerificationEmail(request):
    current_site = get_current_site(request)
    email_subject = 'Activate Your Physics FYP Account'
    email_body = render_to_string('notifications/supervisorConfirm.html', {
        'user': request.user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(request.user.id)),
        'token' : generate_supervisor_token.make_token(request.user),
        'email' : request.user.email 
    })
    send_verification_email.delay(subject = email_subject, body = email_body,  recipient = request.user.email)
    
    return render(request, 'accounts/verificationEmailSent.html')
    



def activate_supervisor(request, uid64, token, email):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        
        user = User.objects.get(id=uid)
    except Exception as e:
        user = None
        
    if user and generate_supervisor_token.check_token(user, token):
        supervisor = Supervisor.objects.get(user = user)
        supervisor.email = email
        user.email = email
        supervisor.verified = True
        supervisor.save()
        user.save()
        email_subject = 'Physics FYP supervisor account created successfully'
        email_body = render_to_string('notifications/welcomesuperv.html', {
            'user': request.user,
            # 'domain': current_site,
            # 'uid': urlsafe_base64_encode(force_bytes(request.user.id)),
            # 'token' : generate_student_token.make_token(request.user),
            # 'email' : email 
        })
        send_verification_email.delay(subject = email_subject, body = email_body,  recipient = supervisor.email)
        messages.add_message(request, messages.SUCCESS, 'Email Verified Successfully')
        return redirect ('verifysupervisor')
    return render(request, 'home/activation_failed.html', {'user': user,})

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
def verifySupervisor(request):
    msg = None
    img_sent = None
    img_verified = None
    form = SupervisorEmailVerificationForm(request.POST or None)
    supervisor = Supervisor.objects.get(user = request.user)
    if supervisor.verified is False:
        if form.is_valid():
            email = form.cleaned_data['email']
            current_site = get_current_site(request)
            email_subject = 'Activate Your Physics FYP Account'
            email_body = render_to_string('notifications/supervisorConfirm.html', {
                'user': request.user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(request.user.id)),
                'token' : generate_supervisor_token.make_token(request.user),
                'email' :email 
            })
            send_verification_email.delay(subject = email_subject, body = email_body,  recipient = email)
            msg = 'Verfication Email Sent Successfully, Please check  your email'
            img_sent = "/img/illustrations/Emailsent.png"
    elif supervisor.verified is True:
        msg = "Your account has been verified successfully."
        img_verified = "/img/illustrations/verified.png"
        
        
    context = {
        'messages': msg,
        'form': form,
        'img1': img_sent,
        'img2' : img_verified
    }
    return render(request, 'home/emailverification.html', context)
    

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
def verifyNewSupervisor(request):
    # msg = None
    # img_sent = None
    img_verified = None
    form = SupervisorEmailVerificationForm(request.POST or None)
    supervisor = Supervisor.objects.get(user = request.user)
    if supervisor.verified is False:
        if form.is_valid():
            email = form.cleaned_data['email']
            current_site = get_current_site(request)
            email_subject = 'Activate Your Physics FYP Account'
            email_body = render_to_string('notifications/supervisorConfirm.html', {
                'user': request.user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(request.user.id)),
                'token' : generate_supervisor_token.make_token(request.user),
                'email' :email 
            })
            send_verification_email.delay(subject = email_subject, body = email_body,  recipient = email)
            return render(request, 'accounts/verificationEmailSent.html')
    elif supervisor.verified is True:
        msg = "Your account has been verified successfully."
        img_verified = "/img/illustrations/verified.png"
        
        
    context = {
        'form': form,
        'img2' : img_verified
    }
    return render(request, 'home/emailverification.html', context)



def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def migratestudents(request, id):
    file = studentData.objects.get(id=id)
    
    df = pd.read_excel(file.file)
    for col in df.columns:
        if col.upper().startswith('I'):
            df.rename(columns = {col: 'indexNumber'}, inplace = True)
        elif 'name' or 'Name' in col:
            df.rename(columns = {col: 'studentName'}, inplace = True)
    json_records = df.reset_index().to_json(orient = 'records')
    data = []
    data  = json.loads(json_records)
    userdata = []
    uses = User.objects.filter(groups__name = 'Student')
    uses.delete()
    for student in data:
        
        surname = student['studentName'].split(',')[0]
        othernames = student['studentName'].split(',')[1]
        username = student['indexNumber']
        indexNo = str( student['indexNumber'])
        user = User (username = indexNo, first_name = othernames, last_name = surname)
        user.set_password(indexNo)
        userdata.append(user)
        user.save()
            
        
        group, created = Group.objects.get_or_create(name = 'Student')
        user.groups.add(group)
        Student.objects.create(user = user, first_name = othernames, last_name = surname, indexNo = indexNo)
    
    file.migrated = True
    file.save()
    studentData.objects.all().delete()
    
    # with open('media/uploads/studentdata.xlsx', mode='r') as csv_file:
    #     csvf = reader(csv_file)
    #     data = []
    #     for Name in csvf:
    #         data.append(Name)
        
        # for Name, Index in csvf:
        #     user = User(username=Index)
        #     user.set_password(Index)
        #     data.append(user)
        #     print(data)
        # User.objects.bulk_create(data)
    
    return redirect('finishedloading')

@method_decorator(verificationRequired, name='dispatch')
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    login_url='login'
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password-success')

@verificationRequired
def passwordSuccess(request):
    email_subject = 'Your password was changed!'
    email_body = render_to_string('accounts/passwordsuccess.html', {
            'user': request.user,
            # 'domain': current_site,
            # 'uid': urlsafe_base64_encode(force_bytes(request.user.id)),
            # 'token' : generate_student_token.make_token(request.user),
            # 'email' : email 
        })
    send_verification_email.delay(subject = email_subject, body = email_body,  recipient = request.user.email)
    msg = 'Password Change Successful'
    img_sent = "/img/illustrations/passwordsucess.png"
    
    
    context = {
        'messages': msg,
        'img1': img_sent,
    }
    return render(request, 'home/emailverification.html', context)



# def forgotPassword(request):
#     form = UserExistForm(request.POST or None)
    
#     if form.is_valid():
#         user = form.cleaned_data['username']
#         User.objects.get(username = user)
#         if user.email:
#             return redirect ('password_reset_confirm')
#         else:
#             return d
        
        
# def noEmailPassword(request):
#     form = NoEmailForm(request.POST or None)
#     if form.is_valid():
#         return redirect ('password_rest_confirm')