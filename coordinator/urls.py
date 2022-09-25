from django.urls import path, re_path
from supervisor.views import supervisordash as sd
from . import views
 
 
urlpatterns = [
    path('coordinator', views.coordinatordash, name = "coordinator"),
    path('coordinator/allprojects', views.codallprojects, name = 'allprojects'),
    path('coordinator/projects/show-all/', views.codshowallprojects, name = 'showallprojects'),
    path('coordinator/allstudents/', views.codallstudents, name = 'allstudents'),
    path('coordinator/all-students/show-all/', views.codallstudentsshow, name ='showallstudents'),
    path('coordinator/all-supervisors/', views.all_supervisors, name = 'all_supervisors'),
    path('coordinator/students/<int:id>/details', views.codstudentdetails, name = 'codstudentdetails'),
    path('coordinator/supervisors/<int:id>/details', views.supervisor_details, name = 'supervisordetails'),
    path('coordinator/supervision', sd, name = 'coordinatorsupervision'),
     path('codcreate', views.codaddproject, name = 'codaddproject'),
    path('coordinator-approve/<int:id>', views.coordinatorapprove, name = 'coordinatorapprove'),
    path('coordinator-decline/<int:id>', views.coordinatordecline, name = 'codecline'),
    path('coordinator/projects/<int:id>/info', views.codpjectinfo, name = 'projectinfo'),
    path('deleteproject/<int:id>', views.deleteproject, name = 'deleteproject'),
    path('coordinator/projects/info/students/<int:id>/remove', views.codapprovestudent, name = 'codapprovestudent'),
    path('coordinator/projects/<int:id>/edit', views.codeditproject, name = 'codeditproject'),
    path('coordinator/project/info/delstudent/<int:id>', views.coddelfrompject, name = 'deletestudentfromproject'),
    path('coordinator/students-data/<int:id>', views.migrateData, name = 'studentdata'),
    path('coordinator/upload-students', views.uploadedData, name = 'UploadStudents'),
    path('coordinator/finished', views.finished, name = 'finishedloading'),
    path('coordinator/search', views.search, name = 'coordinatorsearch'),
    path('coordinator/events/all-events', views.all_events, name = 'allevents'),
    path('coordinator/add-speciailization/', views.addSpecialization, name = 'addspecialization'),
    path('coordinator/events/edit-event/<int:id>', views.edit_event, name = 'edit_event'),
    path( 'coordinator/event/delete-event/<int:id>', views.delete_event, name = 'deleteevent'),
    path('coordinator/notifications/all', views.codNotifications, name = 'codnotifications'),
    path('test', views.test, name = 'test')
    
    
    
 ]