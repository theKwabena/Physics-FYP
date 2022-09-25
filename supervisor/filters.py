import django_filters 
from django import forms
from portal.models import *



class ProjectFilter(django_filters.FilterSet):
    
    specialization = django_filters.ModelChoiceFilter(queryset = Specialization.objects.all(), widget = forms.Select(attrs = {
        "class": "form-control",
    }), empty_label="Search by specialization")
    class Meta:
        model = Project
        fields = ['title', 'specialization']
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
   
    
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'indexNo' ]
        
        
            
class SupervisorFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(widget = forms.TextInput(attrs = {
        "class": "form-control",
        'placeholder': 'Search by first name'
        }),lookup_expr='icontains')
    last_name = django_filters.CharFilter(widget = forms.TextInput(attrs = {
        "class": "form-control",
        'placeholder': 'Search by last name'
        }),lookup_expr='icontains' )
    
    
    
    class Meta:
        model = Supervisor
        fields = ['first_name', 'last_name' ]
             
            
     
def get_project_queryset(request): # updated from `self` to `request`
    queryset = Project.objects.filter(supervisor=request.user.supervisor)
    return queryset
        
class ReportFilter(django_filters.FilterSet):
    project = django_filters.ModelChoiceFilter(queryset = get_project_queryset, widget = forms.Select(attrs = {
        "class": "form-control",
    }), empty_label="Search by specialization")
   
    class Meta:
        model = ProjectReport
        fields = ['name', 'project']
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
        
    # def __init__(self, *args, **kwargs):
    #     self.user = kwargs.pop('user', None)
    #     super(ReportFilter, self).__init__(*args, **kwargs)
    #     self.filters['project'].extra.update({
    #     'queryset': Project.objects.filter(supervisor=self.user.supervisor),
    #     'empty_label': 'Search by project',
    #     'help_text': False,
    #     })
    
       