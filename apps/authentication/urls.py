
from django.urls import path
from .views import login_view, register_user, logoutUser
from django.contrib.auth.views import LogoutView
from landing import views as bs
from . import views

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/step/1/', register_user, name="register"),
    path("logout/", logoutUser, name="logout"),
    path('coordinator/migrate/<int:id>/', views.migratestudents, name = 'migratestudent'),
    path('', bs.homeindex, name = 'Home'),
    path('register/step/2/', views.registerStep2, name = 'regStep2'),
    path('register/step/3/', views.sendVerificationEmail, name = 'regStep3'),
    path('activate-supervisor/<uid64>/<token>/<email>/', views.activate_supervisor, name = 'activate-supervisor'),
    path('verifysupervisoremail/', views.verifySupervisor, name = 'verifysupervisor'),
    path('profile/settings/change-password/',views.PasswordChange.as_view(template_name = 'accounts/changepassword.html'), name = 'change-password'),
    path('password-change-success/', views.passwordSuccess, name = 'password-success')
    
    
]
