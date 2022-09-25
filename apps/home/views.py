# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# from itertools import product
import json
import time
import csv
import xlwt
# from csv import reader
import pandas as pd
from django import template
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from portal.models import *
from .decorators import approvalrequired, unauthenticated_user, allowed_users, registeredstudent
from base.forms import *
from .utils import generate_student_token
from apps.authentication.utils import generate_supervisor_token
from notifications.tasks import send_verification_email
from django.core.paginator import Paginator



# from base.models import *
# from base.forms import *

    


def sedt(request):
    return render(request, 'home/settings.html')


# def supsidebar(request, id):
#     tsupervisor = get_object_or_404(Supervisor, id=id)
#     someid = tsupervisor.id
#     return redirect('superv')









@login_required(login_url='login')
@allowed_users(allowed_roles = ['Student'])
@registeredstudent
@approvalrequired
def stud(request):
    
    student = request.user.student
    tasks = Task.objects.filter(project = student.project)
    events = Event.objects.all().order_by('-date')
    # pnotifs = Notifications.objects.filter(receiver = request.user)
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    chatmessages = ChatMessage.objects.filter(project = student.project)
    if student.project in Project.objects.all():
        mates = Student.objects.filter(project_id =student.project.id ).exclude(id = student.id)
        print (mates)
    else:
        mates = []
    
    
   
    context = {
        'student':student,
        'tasks' : tasks,
        'events': events,
        'mates': mates,
        'chats' : chatmessages,
        # 'room_name' : 'stdnotif',
        # 'personal' : 'notif' + str(request.user.student.indexNo),
        'all_notifs': all_notifs,
        'unread': unread
        
    }
    
    return render(request, 'home/studentview.html', context)

def studentProjectFiles(request):
    student = request.user.student
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    files = ProjectFile.objects.filter(project = request.user.student.project)
    events = Event.objects.all().order_by('-date')
    tasks = Task.objects.filter(project = student.project)
    context = {
        'tasks':tasks,
        'events' : events,
        'files': files,
        'all_notifs': all_notifs,
        'unread': unread,
    }
    
    return render(request, 'home/studentProjectFiles.html', context)
    



def denied(request):
    
    return render(request, 'home/page-403.html')


def pending(request):
    
    return render(request, 'home/projectpendingapproval.html')



def export_data(request):
    
    response = HttpResponse(content_type = 'application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename = ProjectList' + '.xls'
    
    wb = xlwt.Workbook(encoding = 'utf-8')
    ws = wb.add_sheet('Project List')
    row_num = 0
    
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    content_format   = ("alignment: horizontal left, vertical top, wrap on;")
    columns = ['Names', 'Title', 'Supervisor']
    
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns [col_num], font_style)
        
    font_style = xlwt.XFStyle()
    for x in Project.objects.all():
        for i in Student.objects.all():
            if i.project is not None and i.project.id == x.id:
                print(i.first_name,x)
    
    rows = Project.objects.all().values_list('id','title', 'supervisor')
    print(rows)
    for row in rows:
        print(row[0])
        row_num +=1
        for student in Student.objects.all():
            if student.project is not None and student.project.id == row[0]:
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, [str(row[1]), str(student.first_name)], xlwt.easyxf(content_format)) 
    wb.save(response)
    
    return response   


@login_required(login_url='login')
def send_student_activation_email(request):
    msg = None
    img_sent = None
    img_verified = None
    form = EmailVerificationForm(request.POST or None)
    student = Student.objects.get(user = request.user)
    if student.verified is False:
        if form.is_valid(): 
            email = form.cleaned_data['email']
            current_site = get_current_site(request)
            email_subject = 'Activate Your Physics FYP Account'
            email_body = render_to_string('notifications/confirmationemail.html', {
                'user': request.user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(request.user.id)),
                'token' : generate_student_token.make_token(request.user),
                'email' : email 
            })
            send_verification_email.delay(subject = email_subject, body = email_body,  recipient = email)
            msg = 'Verfication Email Sent Successfully, Please check  your email'
            img_sent = "/img/illustrations/Emailsent.png"
    elif student.verified is True:
        msg = 'Your account has been verified successfully. You can now select a project topic'
        img_verified = "/img/illustrations/verified.png"
        
    context = {
        'messages': msg,
        'form': form,
        'img1': img_sent,
        'img2' : img_verified
    }
    return render(request, 'home/emailverification.html', context)

    
    
def activate_student(request, uid64, token, email):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        
        user = User.objects.get(id=uid)
    except Exception as e:
        user = None
        
    if user and generate_student_token.check_token(user, token):
        student = Student.objects.get(user = user)
        student.email = email
        user.email = email
        student.verified = True
        student.save()
        user.save()
        email_subject = 'Account Activated Successfully'
        email_body = render_to_string('notifications/welcomemail.html', {
            'user': request.user,
            # 'domain': current_site,
            # 'uid': urlsafe_base64_encode(force_bytes(request.user.id)),
            # 'token' : generate_student_token.make_token(request.user),
            # 'email' : email 
        })
        send_verification_email.delay(subject = email_subject, body = email_body,  recipient = email)
        messages.add_message(request, messages.SUCCESS, 'Email Verified Successfully')
        return redirect ('verifyemail')
    
    
    return render(request, 'home/activation_failed.html', {'user': user,})




def user_profile_settings(request):
    if request.user.groups.filter(name='Supervisor').exists() or request.user.groups.filter(name='Coordinator').exists() :
        supervisor = Supervisor.objects.get(user=request.user)
        all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
        unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
        form = SupervPicForm(request.POST or None, request.FILES or None, instance = supervisor )
        if request.method == 'POST':
            if form.is_valid():
                form.save()
            rank = request.POST.get('rank')
            supervisor.rank = rank
            supervisor.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
                
                
        
        context = {
            'form' : form,
            'user': supervisor,
            'all_notifs': all_notifs,
            'unread': unread,
        }
        
        return render(request, 'home/supervisorsettings.html', context)
        
    elif request.user.groups.filter(name='Student').exists():
        
        student = Student.objects.get(user = request.user)
        all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
        unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
        form = ProfilePicForm(request.POST, request.FILES, instance = student )
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

            
        
        context = {
            'form': form,
            'user': student,
            'all_notifs': all_notifs,
            'unread': unread,
        }
        return render(request, 'home/studentprofile.html', context)
        
def supervisorVerification(request):
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
    time.sleep(3)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
def sendStudentVerificationEmail(request):
    current_site = get_current_site(request)
    email_subject = 'Activate Your Physics FYP Account'
    email_body = render_to_string('notifications/confirmationemail.html', {
        'user': request.user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(request.user.id)),
        'token' : generate_student_token.make_token(request.user),
        'email' : request.user.email
    })
    send_verification_email.delay(subject = email_subject, body = email_body,  recipient = request.user.email)
    time.sleep(3)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
   
def emailchange(request,user):
    user = request.user
    try:
        request.user.student
        s = Student.objects.get(user=user)
        s.verified = False
        s.save()
        return redirect ('verifyemail')
    except Exception as e:
        print(e)
        s = Supervisor.objects.get(user=user)
        s.verified = False
        s.save()
        return redirect('verifysupervisor')
    
    
    
def ideaSent(request):
    
    
    return render(request, 'home/ideasent.html')


def allnotifications(request, user):
    
    sup_id = request.user.id
    notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator = False).order_by('-datesent')
    # students = Student.objects.filter(project__id__in = stprojects.all())
    # events = Event.objects.all().order_by('-date')      
    p = Paginator(notifs, 10)     
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')[:4]
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    page = request.GET.get('page')
    notifs = p.get_page(page) 
    context = {
        'sid' : sup_id,
        'notifications': notifs,
        'all_notifs': all_notifs,
        'unread': unread
    }
    try:
        request.user.supervisor
        return render(request, 'home/notifications.html', context)
    except Exception as e:
        return render(request, 'home/studentNotifications.html', context)
        
def deleteNotification(request, id):
    notification = Notifications.objects.get(id=id)
    notification.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def delete_for_user(request, id):
    notification = Notifications.objects.filter(receiver_id = id).filter(forcoordinator = False)
    notification.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def studentReport(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    uploads = ProjectReport.objects.filter(sender = request.user.student)
    events = Event.objects.all().order_by('-date')
    tasks = Task.objects.filter(project = request.user.student.project)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = ProjectReport.objects.create(**form.cleaned_data, sender = request.user.student, project = request.user.student.project)
    else:
        form = ReportForm()
    context = {
        'form':form,
        'all_notifs': all_notifs,
        'unread': unread,
        'tasks':tasks,
        'events' : events,
        'uploads' : uploads
    }
    
    return render(request, 'home/submitReport.html', context)


def deleteReport(request,id):
    ProjectReport.objects.get(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



def deleteAccount(request):
    request.user.delete()
    return redirect('Home')