# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
import pandas as pd
import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignUpForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_usersz

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
                    return redirect('supervisor')
                elif user.groups.filter(name = 'Student'):
                    try:
                        if 'projects' in request.GET['next']:
                            url = request.GET['next'].removesuffix('/register')
                            return redirect(url + '/details')
                        elif request.GET['next']:
                            url = request.GET['next']
                            return redirect(url)
                    except Exception as e:
                        return redirect('/')
                    
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})




@unauthenticated_user
def register_user(request):
    msg = None
    form = SignUpForm(request.POST or None)
    if request.POST.get('key') == 'supervisor':
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            
            group = Group.objects.get(name = 'Supervisor')
            user.groups.add(group)
            Supervisor.objects.create(user = user, first_name = form.cleaned_data['first_name'], last_name = form.cleaned_data['last_name'])
            login(request,  user = authenticate(request, username =form.cleaned_data['username'], password = form.cleaned_data['password1']))
            return redirect('Home')
        # else:
        #     msg = 'Form is not valid'
    
    elif request.POST.get('key') == 'coordinator':
        if form.is_valid():
            user =form.save()
            username = form.cleaned_data['username']
            
            group = Group.objects.get(name = 'Coordinator')
            user.groups.add(group)
            group = Group.objects.get(name = 'Supervisor')
            user.groups.add(group)
            
            Supervisor.objects.create(user = user, first_name = form.cleaned_data['first_name'], last_name = form.cleaned_data['last_name'])
            login(request,  user = authenticate(request, username =form.cleaned_data['username'], password = form.cleaned_data['password1']))
            return redirect('Home')
        # else:
        #     msg = 'Form is not valid'
        
    elif request.POST.get('key') == request.POST.get('username'):
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            
            group = Group.objects.get(name = 'Student')
            user.groups.add(group)
            Student.objects.create(user = user, first_name = form.cleaned_data['first_name'], last_name = form.cleaned_data['last_name'])
           
            login(request,  user = authenticate(request, username = form.cleaned_data['username'], password = form.cleaned_data['password1']))
            return redirect('Home')
        # else:
        #     msg = 'Form is not valid'
    else:
        msg = 'Invalid credentials'
        form = SignUpForm()
         
    
    context = {
        'form': form,
        'msg': msg
    }
    
    
    return render(request, 'accounts/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')



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
        user = User (username = indexNo)
        user.set_password(indexNo)
        userdata.append(user)
        user.save()
        
        group = Group.objects.get(name = 'Student')
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
