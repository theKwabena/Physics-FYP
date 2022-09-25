# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from portal.models import Supervisor


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ))
    
    
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Other Names",
                "class": "form-control"
            }
        ))
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')
        
        
    def clean_email(self):
       email = self.cleaned_data.get('email')
       if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email address exists")
       return email
   
   
   
class SupervisorEmailVerificationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Please email your valid and active email",
                "class": "form-control"
            }
        ))
    
    class Meta:
        model = Supervisor
        fields = ['email'] 
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("An account with this email address exists")
        return email
 
class PasswordChangingForm(PasswordChangeForm):
    old_password = forms.CharField(
        label = 'Old Password',
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter Password",
                "class": "form-control"
            }
        ))
    
    new_password1 = forms.CharField(
        label = 'New Password',
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Enter New Password",
                "class": "form-control"
            }
        ))
    new_password2 = forms.CharField(
        label = 'Confirm New Password',
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control",
                'label' : 'Confirm New Password'
            }
        ))

    class Meta:
        model = User
        fields = ('old_password', 'password1', 'password2')
        
        
        