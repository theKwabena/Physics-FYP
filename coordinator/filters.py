import django_filters 
from django import forms
from portal.models import *



class ProjectFilter(django_filters.FilterSet):
    supervisor = django_filters.ModelChoiceFilter(queryset=Supervisor.objects.all(),widget = forms.Select(attrs = {
        "class": "form-control",
    }), empty_label="Search by supervisor")
    specialization = django_filters.ModelChoiceFilter(queryset = Specialization.objects.all(), widget = forms.Select(attrs = {
        "class": "form-control",
    }), empty_label="Search by specialization")
    class Meta:
        model = Project
        fields = ['title', 'specialization', 'supervisor']
        filter_overrides = {
             models.CharField: {
                 'filter_class': django_filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                     'widget': forms.TextInput(attrs={'class': 'form-control',
                                                      'placeholder': 'Search by title'})
                 },
                 
             },
             
            
             
             
            
             
        }
        
        
        
class StudentFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(widget = forms.TextInput(attrs = {
        "class": "form-control",
        'placeholder': 'Search by first name'
        }),lookup_expr='icontains')
    last_name = django_filters.CharFilter(widget = forms.TextInput(attrs = {
        "class": "form-control",
        'placeholder': 'Search by last name'
        }),lookup_expr='icontains' )
    indexNo = django_filters.CharFilter(widget = forms.TextInput(attrs = {
        "class": "form-control",
        'placeholder': 'Search by index number'
        }), lookup_expr='icontains')
    project = django_filters.ModelChoiceFilter(queryset=Project.objects.all(),widget = forms.Select(attrs = {
        "class": "form-control",
        'placeholder': 'search by project'
    }), empty_label='Search by Project', )
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'project', 'indexNo' ]
        
        
            
class SupervisorFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(widget = forms.TextInput(attrs = {
        "class": "form-control",
        'placeholder': 'Search by first name'
        }),lookup_expr='icontains')
    other_names = django_filters.CharFilter(widget = forms.TextInput(attrs = {
        "class": "form-control",
        'placeholder': 'Search by last name'
        }),lookup_expr='icontains' )
    
    
    
    class Meta:
        model = Supervisor
        fields = ['first_name', 'other_names' ]
             
            
     
        
        
               