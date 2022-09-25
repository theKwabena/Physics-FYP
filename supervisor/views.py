import json
import time
from csv import reader
import pandas as pd
from django import template
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.sites.shortcuts import get_current_site
from portal.models import *
from apps.home.decorators import approvalrequired, unauthenticated_user, allowed_users, registeredstudent
from base.forms import *
from csv import reader
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from notifications.notifsender import *
from .filters import *
from apps.authentication.decorators import incompleteRegistration
from coordinator.decorators import verificationRequired




# Create your views here.
@login_required(login_url='login')
@incompleteRegistration
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
def supervisordash(request):
    tsupervisor = request.user.supervisor
    projects = Project.objects.filter(supervisor = request.user.supervisor)
    students = Student.objects.filter(project__id__in = projects.all())
    enrollments = Student.objects.filter(project__id__in = projects.all()).filter(approved = False)
    events = Event.objects.all().order_by('-date')
    tasks = Task.objects.filter(supervisor = tsupervisor)
    selected = Project.objects.filter(supervisor = request.user.supervisor, selected = True)
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False) 
    print(request.user.supervisor.rank)
    
    print(request.user.groups.all())
    
    
    # selected = Project.objects.filter(supervisor = tsupervisor).filter(approve =True)
            
    context = {
        'projects': projects,
        'supervisor':tsupervisor,
        'students': students,
        'selected': selected,
        'events': events,
        'tasks' : tasks,
        'enrollments': enrollments,
        'room_name': 'supervisornotifications',
        'all_notifs': all_notifs,
        'unread': unread
       
       
    }
    
    return render(request, 'home/supervisor.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
@verificationRequired
def supaddproject(request):
    form = approveForm(request.POST or None)
    projects = Project.objects.filter(supervisor = request.user.supervisor)
    events = Event.objects.all().order_by('-date')
    suprojects = Project.objects.filter(supervisor = request.user.supervisor)
    student = Student.objects.filter(project__id__in = suprojects.all())
    supervisor = Supervisor.objects.get(user =request.user)
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False) 
    supervisors = Supervisor.objects.filter(role = 'Project Coordinator')
    
    if form.is_valid():
        s = Project.objects.create(**form.cleaned_data, supervisor = request.user.supervisor)
        subject = str(supervisor.rank.title() + ' ' + supervisor.first_name.title() + ' ' + supervisor.other_names.title() + ' added a new project')
        message = str(supervisor.rank.title() + ' ' + supervisor.first_name.title() + ' ' + supervisor.other_names.title() + ' added a new project,  go to your dashboard to approve')
        current_site = get_current_site(request)
        email_subject = subject
        for superv in supervisors:
            if not superv.id == supervisor.id:
                email_body = render_to_string('notifications/newprojectemail.html', {
                            'supervisorName' : superv,
                            'name': str( supervisor.rank + ' ' + supervisor.first_name + ' ' + supervisor.other_names),
                            'domain': current_site,
                            'project' : s.title
                        })
                send_codPersonal(request.user.id, 'Supervisor', message, superv.id, email_subject,  email_body)
        return redirect('supervisorall')
      
       
          
    context = {
        'projects': projects,
        'form':form,
        'events':events,
        'students': student,
        'codprojects': suprojects,
        'room_name': 'supervisornotifications',
        'all_notifs': all_notifs,
        'unread': unread
    }
    
    return render(request, 'home/supaddproject.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
def supaddtask(request):
    tsupervisor = request.user.supervisor
    sttasks = Task.objects.filter(supervisor = tsupervisor).order_by('completed').distinct()
    # students = Student.objects.filter(project__id__in = stprojects.all())
    events = Event.objects.all().order_by('-date') 
    projects = Project.objects.filter(supervisor = request.user.supervisor)     
    p = Paginator(sttasks, 10)
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')[0:4]
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False) 
    page = request.GET.get('page')
    tasks = p.get_page(page)
    form = TaskForm(user = request.user, data = request.POST or None)
    if form.is_valid():
        name = form.cleaned_data['name']
        project = form.cleaned_data['project']
        Task.objects.create(name = name, project = project,supervisor = request.user.supervisor)
        return redirect ('alltasks')
        
    
    context = {
        'form' : form,
        'tasks':tasks,
        'supervisors':tsupervisor,
        'room_name': 'supervisornotifications',
        'all_notifs': all_notifs,
        'unread': unread,
        'events' : events,
        'projects' : projects
    }
    
    return render(request, 'home/supaddtask.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
def marktaskcomplete(request, id):
    task = Task.objects.get(id=id)
    task.completed = True
    task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
def deleteTask(request, id):
    task = Task.objects.get(id=id)
    task.delete()
    # task.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
def supallprojects(request):
    tsupervisor = request.user.supervisor
    stprojects = Project.objects.filter(supervisor = request.user.supervisor)
    students = Student.objects.filter(project__id__in = stprojects.all())
    events = Event.objects.all().order_by('-date') 
    
    # projects = Project.objects.all().order_by('-date_updated')
    projectfilter = ProjectFilter(request.GET, queryset = stprojects) 
    projects = projectfilter.qs
    
         
    p = Paginator(projects.filter(supervisor = request.user.supervisor), 10)
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False) 
    
    page = request.GET.get('page')
    projects = p.get_page(page)
    
    context = {
        'projects':projects,
        'supervisors':tsupervisor,
        'projectfilter': projectfilter,
        'students':students,
        'room_name': 'supervisornotifications',
        'all_notifs': all_notifs,
        'unread': unread
    }
    return render(request, 'home/supervisorall.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
@verificationRequired
def supervisoraccept(request,id):
    student = Student.objects.get(id=id)
    project = Project.objects.get(id = student.project.id)
    student.approved = True
    project.selected = True
    student.save()
    if project.slots <= 0:
        project.occupied = True
        project.save()
    project.save()
    subject = str('Your project enrollment has been approved!')
    message = str( project.supervisor.rank.title() + ' ' + project.supervisor.first_name + ' ' + project.supervisor.other_names +' approved your project enrollment')
    current_site = get_current_site(request)
    email_subject = subject
    email_body = render_to_string('notifications/supapprovemail.html', {
                'supervisorName' : project.supervisor,
                'domain': current_site,
                'name': student,
                'project' : project
            })
    send_student(request.user.id,'Supervisor', message, student.id, email_subject, email_body)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
@verificationRequired
def supervisordecline(request,id):
    student = Student.objects.get(id=id)
    project = Project.objects.get(id=student.project.id)
    student.project = None
    student.approved = False
    student.save()
    if project.slots < 0:
        project.slots = 0
        project.selected = False
        project.save()
    project.slots+=1
    project.occupied = False
    project.save()
    subject = str('Your project enrollment has been declined!')
    message = str( project.supervisor.rank.title() + ' ' + project.supervisor.first_name + ' ' + project.supervisor.other_names +' declined your enrollment')
    email_subject = subject
    email_body = render_to_string('notifications/supdeclineproject.html', {
                'supervisorName' : project.supervisor,
                'name': student,
                'project' : project
            })
    send_student(request.user.id,'Supervisor', message, student.id, email_subject, email_body)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
@verificationRequired
def suppjectinfo(request, id):
    supervisor = request.user.supervisor
    project = Project.objects.get(id = id)
    projectFiles = ProjectFile.objects.filter(project = project)
    students = Student.objects.filter(project = project)
    chats = ChatMessage.objects.filter(project = project)
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False) 
    # print(students)
    context = {
        'projectFiles': projectFiles,
        'project': project,
        'students' : students,
        'supervisor' : supervisor,
        'all_notifs': all_notifs,
        'unread': unread,
        'chats' : chats,
    }
    return render(request, 'home/supprojectinfo.html', context)


    
@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
@verificationRequired    
def supeditproject(request,id):
    project = Project.objects.get(id=id)
    projectFiles = ProjectFile.objects.filter(project = project)
    events= Event.objects.all()

    form = editForm(request.POST or None, instance = project)
    students = Student.objects.filter(project_id = project.id)
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False) 
    if form.is_valid():
        form.save()
        time.sleep(3)
        return redirect(suppjectinfo, id =id)
        
        
    else:
        form = editForm(request.POST or None, instance = project)
    context = {
        'events' : events,
        'projectFiles': projectFiles,
        'project':project,
        'form': form,
        'students': students,
        'all_notifs': all_notifs,
        'unread': unread
    }
    
    return render(request, 'home/supeditproject.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration 
@verificationRequired
def supdelfrompject(request,id):
    student = Student.objects.get(id=id)
    pid = student.project.id
    project = Project.objects.get(id=pid)
    student.project = None
    student.approved = False
    student.save()
    project.occupied -=1
    project.save()
    subject = str('Your have been removed from your project group!')
    message = str( project.supervisor.rank.title() + ' ' + project.supervisor.first_name + ' ' + project.supervisor.other_names +' removed you from project group')
    email_subject = subject
    email_body = render_to_string('notifications/supremove.html', {
                'supervisorName' : project.supervisor,
                'name': student,
                'project' : project
            })
    send_student(request.user.id,'Supervisor', message, student.id, email_subject, email_body)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration 
def supstudents(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False) 
    projects = Project.objects.filter(supervisor = request.user.supervisor)
    students =Student.objects.filter(project__id__in = projects.all())
    studentFilter = StudentFilter(request.GET, queryset = students)
    students = studentFilter.qs
    s = Paginator(students, 10)
    page = request.GET.get('page')
    students = s.get_page(page)
    
    
    context = {
        'projects' : projects,
        'students' : students,
        'studentfilter': studentFilter,
        'all_notifs': all_notifs,
        'unread': unread
    }
    
    return render(request, 'home/supervisorallstudents.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration 
def supstddetails(request, id):
    student = Student.objects.get(id=id)
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False) 
    # file = studentData.objects.order_by('-date_uploaded').first()
   
    
    context = {
        'student': student,
        'all_notifs': all_notifs,
        'unread': unread
        
    }
    
    return render(request, 'home/supstudentdetails.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
def supervisorPitchedTopics(request):
    pitchedTopics = pitchedTopic.objects.all()
    p = Paginator(pitchedTopics, 10)
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False)  
    
    
    page = request.GET.get('page')
    projects = p.get_page(page)   
 
    
    context = {
        'projects' : projects,
        'all_notifs': all_notifs,
        'unread': unread
    }
    return render(request, 'home/pitchedTopics.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration 
@verificationRequired
def supervisorApprovePitched(request, id):
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False) 
    initdata = pitchedTopic.objects.get(id=id)
    student = initdata.sender
    
    form = approveForm(request.POST or None,  instance = initdata)
    if form.is_valid():
        project = Project.objects.create(**form.cleaned_data, supervisor = request.user.supervisor, selected = True )
        student.project = project
        student.approved = True
        student.save()
        initdata.delete()
        form = approveForm()
        subject = str('Your pitched project enrollment has been approved!')
        message = str( project.supervisor.rank.title() + ' ' + project.supervisor.first_name + ' ' + project.supervisor.other_names +' approved your project idea')
        current_site = get_current_site(request)
        email_subject = subject
        email_body = render_to_string('notifications/supapprovemail.html', {
                    'supervisorName' : project.supervisor,
                    'domain': current_site,
                    'name': student,
                    'project' : project
                })
        send_student(request.user.id,'Supervisor', message, student.id, email_subject, email_body)
        return redirect('supervisorall')
          
    context = {
        'form':form,
        'all_notifs': all_notifs,
        'unread': unread
    }
    
    return render(request, 'home/supaddproject.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
def supervisorProjectFiles(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False) 
    events = Event.objects.all().order_by('-date')
    project = Project.objects.filter(supervisor = request.user.supervisor)
    uploads = ProjectFile.objects.filter(project__id__in = project.all())
    form = ProjectFileForm(request.POST or None, request.FILES or None, user = request.user)
    if form.is_valid():
        report = ProjectFile.objects.create(**form.cleaned_data)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
    context = {
        'form':form,
        'all_notifs': all_notifs,
        'unread': unread,
        'uploads' : uploads,
        'events' : events,
        'projects' :project
    }
    
    return render(request, 'home/uploadprojectfile.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
def deleteProjectFile(request,id):
    ProjectFile.objects.get(id=id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration
def submittedReport(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).filter(forcoordinator=False).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(forcoordinator = False).filter(read = False) 
    events = Event.objects.all().order_by('-date')
    projects = Project.objects.filter(supervisor = request.user.supervisor)
    reports = ProjectReport.objects.filter(project__id__in = projects.all())
    reportFilter = ReportFilter(request.GET, queryset = reports, request= request)
    reports = reportFilter.qs
    print(reports)
    
    
    context = {
        'reports' : reports,
        'reportFilter': reportFilter,
        'unread': unread,
        'all_notifs' : all_notifs        
    }
    
    return render(request, 'home/supSubmittedReports.html', context)
    
    
@login_required(login_url='login')
@allowed_users(allowed_roles = ['Supervisor', 'Coordinator'])
@incompleteRegistration 
@verificationRequired   
def supervisorChatRoom(request):
    supervisor = request.user.supervisor
    projects = Project.objects.filter(supervisor = supervisor)
    
    context = {
        'projects' : projects
    }
    
    return render(request, 'home/supervisorChat.html', context)