from django.urls import path
from .views import *



urlpatterns = [
    path('projects/', home, name = 'projects'),
    path('projects/<pk>/details/', projectdetail.as_view(), name = 'projectdetail'),
    path('projects/<int:id>/register/', studentUpdate, name = 'studentupdate' ),
    path('allprojects/',all_projects, name = 'portalallprojects' ),
    path('projects/category/<str:cats>/all/', category, name ='category'),
    path('search/', search, name = 'portalsearch'),
    path('pitch/', PitchTopic, name = 'pitchprojecttopic'),
    path('specializations/', specPage, name = 'specPage'),
    path('supervisors/', supervisorsPage, name = 'supervPage'),
    path('supervisors/<str:fname>-<str:onames>/<int:id>/all/', sortbysuperv, name = 'supervisorProjects')
    # path('tw/', twtry, name = 'tailwind'),
    # path('appr/<int:id>', approve, name = 'approve')
]
