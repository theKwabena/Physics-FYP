import json
import datetime as dt
import time
from csv import reader
import pandas as pd
from django import template
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from portal.models import *
from notifications.notifsender import send_general as sn
from .decorators import approvalrequired, unauthenticated_user, allowed_users, registeredstudent, verificationRequired
from base.forms import *
from csv import reader
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.core.paginator import Paginator
from .filters import *
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from notifications.notifsender import *

# Create your views here.

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator'])   
def coordinatordash(request):
    allstudent = Student.objects.all()
    projects= Project.objects.all().order_by('-approved').order_by('-date_updated')
    supervisors = Supervisor.objects.all()
    specializations = Specialization.objects.all()
    # coprojects = Project.objects.filter(supervisor = request.user.supervisor)
    # student = Student.objects.filter(project__id__in = coprojects.all())
    events = Event.objects.all().order_by('-date')
    stdwithprojects = Student.objects.filter(approved = 'True')
    all_notifs = Notifications.objects.filter(receiver = request.user, forcoordinator = True).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    # print (Notifications.objects.filter(receiver_id = 37))
    # supervisor_notifs = Notifications.objects.filter(msgtype = 'Supervisors')
    # print(allnotifs)
    
    
    
    context = {
        'projects': projects,
        'supervisors': supervisors,
        # 'codprojects': coprojects,
        'students': stdwithprojects,
        'events': events,
        'specializations' : specializations,
        'allstudents': allstudent,
        'room_name' : 'broadcast',
        'all_notifs': all_notifs,
        'unread': unread
    }
    return render(request, 'home/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
@verificationRequired
def codallprojects(request):
    # projects= Project.objects.all().order_by('-date_updated')
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    supervisors = Supervisor.objects.all()
    # students = Student.objects.filter(project__id__in = projects.all())
    students = Student.objects.filter(approved = True )
    
    projects = Project.objects.all().order_by('-date_updated')
    projectfilter = ProjectFilter(request.GET, queryset = projects) 
    projects = projectfilter.qs
    
    p = Paginator(projects.order_by('-date_updated'), 10)
    page = request.GET.get('page')
    projects = p.get_page(page)
    numb = 'a' * projects.paginator.num_pages
    
    
    context = {
        'projects': projects,
        'supervisors': supervisors,
        'students': students,
        'numbs': numb,
        'projectfilter': projectfilter,
        'all_notifs': all_notifs,
        'unread': unread
    }
    return render(request, 'home/allprojects.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def codshowallprojects(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    # projects= Project.objects.all().order_by('-date_updated')
    supervisors = Supervisor.objects.all()
    projects = Project.objects.all().order_by('-date_updated')
    projectfilter = ProjectFilter(request.GET, queryset = projects)
    projects = projectfilter.qs
    students = Student.objects.filter(approved = True )
    p = Paginator(projects, projects.count())
    page = request.GET.get('page')
    projects = p.get_page(page)
    numb = 'a' * projects.paginator.num_pages
    
    
    context = {
        'projects': projects,
        'supervisors': supervisors,
        'students': students,
        'numbs': numb,
        'projectfilter': projectfilter,
        'all_notifs': all_notifs,
        'unread': unread
    }
    return render(request, 'home/allprojects.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def codaddproject(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    form = approveForm(request.POST or None, request.FILES or None)  
    allstudent = Student.objects.all()
    projects= Project.objects.all().order_by('-date_updated')
    supervisors = Supervisor.objects.all()
    coprojects = Project.objects.filter(supervisor = request.user.supervisor)
    student = Student.objects.filter(project__id__in = coprojects.all())
    events = Event.objects.all().order_by('-date')
    
    if form.is_valid():
        Project.objects.create(**form.cleaned_data, supervisor = request.user.supervisor)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  
       
          
    context = {
        'projects': projects,
        'supervisors': supervisors,
        'codprojects': coprojects,
        'students': student,
        'events': events,
        'allstudents': allstudent,
        'form':form,
        'all_notifs': all_notifs,
        'unread': unread
    }
    
    return render(request, 'home/codaddprojectview.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def codpjectinfo(request, id):
    project = Project.objects.get(id = id)
    students = Student.objects.filter(project_id = project.id)
    slots = project.slots-project.occupied
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    context = {
        'project': project,
        'students' : students,
        'slot' : slots,
        'all_notifs': all_notifs,
        'unread': unread
    }
    return render(request, 'home/projectinfo.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def codapprovestudent(request,id):
    student = Student.objects.get(id=id)
    project = Project.objects.get(id = student.project.id)
    student.approved = True
    project.occupied-=1;
    student.save()
    project.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def codeditproject(request,id):
    project = Project.objects.get(id=id)
    form = editForm(request.POST or None, request.FILES or None,instance = project)
    students = Student.objects.filter(project_id = project.id)
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    if form.is_valid():
        form.save()
        time.sleep(3)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        
    else:
        form = editForm(request.POST or None, instance = project)
    context = {
        'project':project,
        'form': form,
        'students': students,
        'all_notifs': all_notifs,
        'unread': unread
    }
    
    return render(request, 'home/codeditproject.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def coddelfrompject(request,id):
    student = Student.objects.get(id=id)
    pid = student.project.id
    project = Project.objects.get(id=pid)
    student.project = None
    student.approved = False
    student.save()
    project.occupied -=1
    project.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/')) 
 

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator'])    
def coordinatorapprove(request, id):
    project = Project.objects.get(id=id)
    supervisor = Supervisor.objects.get(id = request.user.supervisor.id)
    project.approved = True
    project.save()
    subject = str('Project topic approved!')
    message = str(supervisor.rank.title() + ' ' + supervisor.first_name + ' ' +  supervisor.other_names + ' approved ' + project.title)
    current_site = get_current_site(request)
    email_subject = subject
    email_body = render_to_string('notifications/codapproveprojectemail.html', {
                'supervisorName' : supervisor,
                'receiverName' : project.supervisor,
                'domain': current_site,
                'name': str(project.supervisor.first_name + ' ' + project.supervisor.other_names),
                'project' :project.title
            })
    send_supervisor(project.id,request.user.id, 'Coordinator', email_subject,  email_body, message)
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def coordinatordecline(request,id):
    project = Project.objects.get(id=id)
    supervisor = Supervisor.objects.get(id = project.supervisor.id)
    coordinator = Supervisor.objects.get(user = request.user.id)
    
    
    subject = str('Sorry, your project topic has been declined!')
    message = str( coordinator.first_name + ' ' + coordinator.other_names +' declined your project enrollment')
    current_site = get_current_site(request)
    email_subject = subject
    email_body = render_to_string('notifications/coddeclineprojectmail.html', {
                'supervisor' : supervisor,
                'supervisorName' : coordinator,
                'domain': current_site,
                'name': str(supervisor.first_name + ' ' + supervisor.other_names),
                'project' : project
            })
    send_supervisor(project.id,request.user.id, 'Coordinator', email_subject,  email_body, message)
    project.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def codallstudents(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    projects= Project.objects.all().order_by('-date_updated')
    supervisors = Supervisor.objects.all()
    students = Student.objects.all()
    studentFilter = StudentFilter(request.GET, queryset = students)
    students = studentFilter.qs
    s = Paginator(students.order_by('first_name'), 10)
    
    page = request.GET.get('page')
    students = s.get_page(page)
    numb = 'a' * students.paginator.num_pages
    
    context = {
        'projects': projects,
        'supervisors': supervisors,
        'students' : students,
        'numbs': numb,
        'studentfilter': studentFilter,
        'all_notifs': all_notifs,
        'unread': unread
    }
    return render(request, 'home/allstudents.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def codallstudentsshow(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    projects= Project.objects.all().order_by('-date_updated')
    supervisors = Supervisor.objects.all()
    students = Student.objects.all()
    s = Paginator(Student.objects.all().order_by('-first_name'), students.count())
    page = request.GET.get('page')
    students = s.get_page(page)
    numb = 'a' * students.paginator.num_pages
    
    context = {
        'projects': projects,
        'supervisors': supervisors,
        'students' : students,
        'numbs': numb,
        'all_notifs': all_notifs,
        'unread': unread
    }
    return render(request, 'home/allstudents.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def all_supervisors(request):
    supervisors = Supervisor.objects.all()
    supervisorFilter = SupervisorFilter(request.GET, queryset =supervisors)
    supervisors = supervisorFilter.qs 
    s = Paginator(supervisors.order_by('-other_names'), 15)
    
    page = request.GET.get('page')
    supervisors = s.get_page(page)
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    
    context = {
        'supervisors': supervisors,
        'all_notifs': all_notifs,
        'unread': unread,
        'supervisorfilter':supervisorFilter
    }
    
    return render(request, 'home/allsupervisors.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def supervisor_details(request, id):
     supervisor = Supervisor.objects.get(id=id)
     project = Project.objects.filter(supervisor = supervisor)
     students = Student.objects.filter(project__id__in = project.all())
     all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
     unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
     
     
     context = {
         'supervisor' : supervisor,
         'projects' : project,
         'students' : students,
         'all_notifs': all_notifs,
         'unread': unread,
         
         
     }
     
     return render (request, 'home/supervisordetails.html', context)
    

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator', 'Supervisor']) 
def coddelstudent(request,id):
    student = Student.objects.get(id = id)
    student.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
 
 

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator'])    
def deleteproject(request, id):
    project = Project.objects.get(id=id)
    supervisor = Supervisor.objects.get(id = project.supervisor.id)
    coordinator = Supervisor.objects.get(user = request.user.id)
    
    
    subject = str('Your project topic has been deleted!')
    message = str( coordinator.first_name + ' ' + coordinator.other_names +' declined your project enrollment')
    current_site = get_current_site(request)
    email_subject = subject
    email_body = render_to_string('notifications/coddeleteprojectemail.html', {
                'supervisor' : supervisor,
                'supervisorName' : coordinator,
                'domain': current_site,
                'name': str(supervisor.first_name + ' ' + supervisor.other_names),
                'project' : project
            })
    send_supervisor(project.id,request.user.id, 'Coordinator', email_subject,  email_body, message)
    project.delete()
    return redirect('allprojects')




@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def all_events(request):
    events = Event.objects.all()
    s = Paginator(events,10)
    page = request.GET.get('page')
    events = s.get_page(page)
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
    
    context = {
        'form':form,
        'events' : events,
        'all_notifs': all_notifs,
        'unread': unread
    }
    
    return render(request, 'home/events.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def edit_event(request, id):
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    init = Event.objects.get(id=id)
    form = EventForm(request.POST or None, instance = init)
    if form.is_valid():
        form.save()
        
        redirect('coordinator')
    context = {
        'form':form,
        'all_notifs': all_notifs,
        'unread': unread
    }
    return render(request, 'home/addevent.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def delete_event(request, id):
    event = Event.objects.get(id=id)
    event.delete()
    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))



@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def migrateData(request,id):
    
    file = studentData.objects.get(id=id)
    df = pd.read_excel(file.file)
    for col in df.columns:
        if 'index' in col or col.upper().startswith('I') or col.upper() == 'INDEX':
            df.rename(columns = {col: 'indexNumber'}, inplace = True)
        elif 'name' or 'Name' in col:
            df.rename(columns = {col: 'studentName'}, inplace = True)
    # print(df)
    json_records = df.reset_index().to_json(orient = 'records')
    data = []
    data  = json.loads(json_records)
    
    file.save()
    return render(request, 'home/studentdata.html', {'data': data, 'file': file})


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def uploadedData(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    files = studentData.objects.all().order_by('-date_uploaded')
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            n = studentData.objects.create(file = request.FILES['file'])
            
            # Redirect to the document list after POST
            return redirect(migrateData, n.pk)
    else:
        form = DocumentForm()
    context = {
        'files': files,
        'form' : form,
        'all_notifs': all_notifs,
        'unread': unread
    }
    return render(request, 'home/uploadstudents.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def codstudentdetails(request, id):
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    
    student = Student.objects.get(id=id)
    file = studentData.objects.order_by('-date_uploaded').first()
   
    
    context = {
        'student': student,
        'all_notifs': all_notifs,
        'unread': unread
        
    }
    
    return render(request, 'home/codstudentdetails.html', context)

 

def test(request):
    
    sn('general', request.user.id, 'This is a message to all users of this platform')
    # sn('coordinator', request.user.id, 'Student', 'This to your email as project coordinator')
    return HttpResponse('Done')


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def finished(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    projects= Project.objects.all().order_by('-date_updated')
    supervisors = Supervisor.objects.all()
    students = Student.objects.all().order_by('first_name')
    
    
    context = {
        'projects': projects,
        'supervisors': supervisors,
        'students' : students,
        'all_notifs': all_notifs,
        'unread': unread
    }
    return render(request, 'home/finished.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def search(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    if request.method == 'POST':
        searched = request.POST['searched']
        projects = Project.objects.filter(Q(title__icontains=searched)|Q(description__icontains = searched))
        events = Event.objects.filter(name__icontains = searched)
        students = Student.objects.filter(Q(first_name__icontains=searched)|Q(last_name__icontains=searched))
        supervisors = Supervisor.objects.filter((Q(first_name__icontains=searched)|Q(other_names__icontains=searched)) |Q(email__icontains = searched))
        pitchedtopics = pitchedTopic.objects.filter(title__icontains = searched)
        
        context ={
            'students' : students,
            'searched': searched,
            'projects': projects,
            'events' : events,
            'students' : students,
            'supervisors' : supervisors,
            'pitchedTopics' : pitchedtopics,
            'all_notifs': all_notifs,
            'unread': unread
        }
        return render(request, 'home/search.html', context)
    else:
        context = {
            'all_notifs': all_notifs,
            'unread': unread
        }
        return render(request, 'home/search.html', context)
    


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def codNotifications(request):
    sup_id = request.user.id
    notifs = Notifications.objects.filter(receiver = request.user, forcoordinator = True).order_by('datesent')
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
    return render(request, 'home/codnotifications.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles = ['Coordinator']) 
def addSpecialization(request):
    all_notifs = Notifications.objects.filter(receiver = request.user).order_by('-datesent')
    unread = Notifications.objects.filter(receiver =request.user).filter(read = False)
    events = Event.objects.all().order_by('-date')
    form = SpecializationForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('coordinator')
        
    context = {
        'form':form,
        'all_notifs': all_notifs,
        'unread': unread,
        'events':events
    }
    
    return render(request, 'home/addspecialization.html', context)
