
from django.urls import path, re_path
from apps.home import views
from . import views

urlpatterns = [
    path('supervisor/', views.supervisordash, name = 'supervisor' ),
    path('supervisor/allprojects/', views.supallprojects, name = 'supervisorall'),
    path('supervisor/project-topics/pitched-by-students', views.supervisorPitchedTopics, name = 'pitched'),
    # path('std', views.stud, name='studentview'),
   
    path('supervisor/addproject', views.supaddproject, name = 'supaddproject'),
    path('supervisor/tasks-all', views.supaddtask, name = 'alltasks'),
    path('supervisor/approve-student/<int:id>', views.supervisoraccept, name = 'supervisoraccept'),
    path('supervisor-decline/<int:id>', views.supervisordecline, name = 'supervisordecline'),
    path('supervisor/mark-task-as-complete/<int:id>', views.marktaskcomplete, name = 'marktaskcomplete'),
    path('supervisor/delete-task/<int:id>', views.deleteTask, name = 'deletetask'),
    
    path('supervisor/project/info/<int:id>', views.suppjectinfo, name = 'supprojectinfo'),
    path('supervisor/project/info/edit/<int:id>', views.supeditproject, name = 'supeditproject'),
    path('supervisor/project/info/delstudent/<int:id>', views.supdelfrompject, name = 'supdeletestudentfromproject'),
    path('supervisor/students-under-me', views.supstudents, name = 'studentsunderme'),
    path('supervisor/students/<int:id>/details', views.supstddetails, name = 'supstudentdetails'),
    path('supervisor/project-files/', views.supervisorProjectFiles, name = 'projectfiles'),
    path('supervisor/project-files/delete/<int:id>/', views.deleteProjectFile, name = 'deleteProjectFile'),
    path('supervisor/reports/', views.submittedReport, name = 'submittedReports'),
    path('supervisor/projects/approve-topic-by-student/<int:id>', views.supervisorApprovePitched, name = 'approvepitched')
    
]