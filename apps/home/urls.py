# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
# from supervisor import views
from apps.home import views

urlpatterns = [

   
    # path('sup/<int:id>', views.supsidebar, name = 'supsidebar'),
    
    # path('supervisor/', views.supervisordash, name = 'supervisor' ),
    # path('supervisor/allprojects/', views.supallprojects, name = 'supervisorall'),
    path('student/', views.stud, name='studentview'),
    # path('codcreate', views.codaddproject, name = 'codaddproject'),
    # path('supervisor/addproject', views.supaddproject, name = 'supaddproject'),
    # path('approve-student/<int:id>', views.supervisoraccept, name = 'supervisoraccept'),
    
   
    path('access-denied/', views.denied, name = 'denied'),
    # path('un-verified'),
    path('pending-approval/', views.pending, name = 'pending'),
    path('verifyemail/', views.send_student_activation_email, name = 'verifyemail'),
    path('activate-student/<uid64>/<token>/<email>/', views.activate_student, name = 'activate-student'),
    path('profile/settings/', views.user_profile_settings, name = 'settings'),
    path('export/', views.export_data, name = 'export'),
    path('pitch-idea/idea-sent-success/', views.ideaSent, name = 'ideasent'),
    path('delete-notification/<int:id>/', views.deleteNotification, name = 'deletenotif'),
    path('delete-for-user/<int:id>/', views.delete_for_user, name = 'deleteforuser'),
    path('<str:user>/notifications/', views.allnotifications, name = 'notifications'),
    path('student/submit-report/', views.studentReport, name = 'submitreport'),
    path('student-delete-report/<int:id>/', views.deleteReport, name = 'deleteReport'),
    path('student/project-files/', views.studentProjectFiles, name = 'studentProjectFiles'),
    path('<slug:user>/change-email/', views.emailchange, name = 'changeEmail'),
    path('send-student-verification/', views.sendStudentVerificationEmail, name = 'verifystudentemail'),
    path('send-supervisor-verification/',views.supervisorVerification, name = 'sendsupervVerify' ),
    path('delete-account/', views.deleteAccount, name = "delete-account")
    


    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),

]
