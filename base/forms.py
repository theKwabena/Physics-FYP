from dataclasses import field, fields
from faulthandler import disable
from django import forms
from django.contrib.auth.models import User

from portal.models import Project, Event, ProjectReport, Specialization, Student, pitchedTopic, studentData, Task, ProjectFile, Supervisor

class approveForm(forms.ModelForm):
    title = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control",
        "label": "email"
    }))
    
    description = forms.CharField(widget = forms.Textarea(attrs={
        "class":"form-control" ,
        "id": "textarea"
    }))
    
    slots = forms.IntegerField(widget = forms.NumberInput(attrs={
        "class":"form-control" ,
        "id": "textarea"
    }))
    
 
   
    class Meta:
        model = Project
        fields = [
            'title', 'description','specialization', 'projectimg', 'slots'
        ]
        
        widgets = {
            'specialization':forms.Select(attrs = {
                'class': "form-select",
                'empty_label': 'Please select Specliaization',
                'label': 'Select',
                'id': 'country',
                'aria-label': 'Select'
                
                
            }),
            
        #     'supervisor': forms.Select(attrs = {
        #         'class': "form-select",
        #         'empty_label': 'Please select Specliaization',
        #         'label': 'Select',
        #         'id': 'country',
        #         'aria-label': 'Select'
        # }),
            
            'projectimg': forms.ClearableFileInput(attrs = {
                "class": "form-control",
                "id": "formFile",
                'label': 'Project Image (optional)'
            })
            
        }
        
        
        labels = {
            'projectimg' : 'Project Image (Optional)'
        }
    

class editForm(forms.ModelForm):
    title = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control",
        "label": "title"
    }))
    
    description = forms.CharField(widget = forms.Textarea(attrs={
        "class":"form-control" ,
        "id": "textarea"
    }))
    
 
    
    class Meta:
        model = Project
        fields = [
            'title', 'description','specialization', 'projectimg'
        ]
        
        widgets = {
            'specialization':forms.Select(attrs = {
                'class': "form-select",
                'empty_label': 'Please select Specliaization',
                'label': 'Select',
                'id': 'country',
                'aria-label': 'Select'
                
                
            }),
            
            
            'projectimg': forms.ClearableFileInput(attrs = {
                "class": "form-control",
                "id": "formFile",
                'label': 'Project Image (optional)'
            })
            
        }
        
        
        labels = {
            'projectimg' : 'Project Image (Optional)'
        }
     
class EventForm(forms.ModelForm):
    date = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control",
        'id' : 'date_selector',
        'type' : 'date'
       
    }))
    
    name = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control",
      
        'placeholder': 'Please enter event name',

    }))
    
    
    class Meta:
        model = Event
        fields = [
            'name',
            'date',
        ]
        
   
        
        
class StudentRegistration(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'indexNo',
            
        ]   
        
        
        widgets = {
            'first_name':forms.TextInput(attrs = {
                'class': "form-control",
                'placeholder': 'Enter First Name'
                # 'aria-label': 'Select'
                
                
            }),
            
            'last_name': forms.TextInput(attrs = {
                'class': "form-select",
                'empty_label': 'Please select Specliaization',
                'label': 'Select',
                'id': 'country',
                'aria-label': 'Select'
        }),
            
           'indexNo': forms.TextInput(attrs = {
                'class': "form-control",
                'empty_label': 'Please select Specliaization',
                'label': 'Select',
                'id': 'country',
                'aria-label': 'Select'
        }),
           
            
        }
        
        
        labels = {
            'projectimg' : 'Project Image (Optional)'
        }
    
        
class DocumentForm(forms.ModelForm):
    
    
    class Meta:
        model = studentData
        fields = [
                'file'
            ]
        
        widgets = {
            'file': forms.ClearableFileInput(attrs = {       
            'class': "form-control",
            
            
                    
                    
                })
            }
        
        labels = {
            'file' : 'Select Student Data File'
        }
   
        
class EmailVerificationForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Please email your valid and active email",
                "class": "form-control"
            }
        ))
    
    class Meta:
        model = Student
        fields = ['email']  
        
        
        
class PitchedForm(forms.ModelForm):
    title = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control",
        "placeholder": "Have a title?"
    }))
    
    description = forms.CharField(widget = forms.Textarea(attrs={
        "class":"form-control" ,
        "id": "textarea",
        'placeholder': 'Tell supervisors your project idea'
    }))   
    
    class Meta:
        model = pitchedTopic
        fields = ['title', 'description'] 
# class studentRegisterForm(forms.ModelForm):
#     title = forms.CharField(widget = forms.TextInput(attrs = {
#         "class": "form-control",
#         "label": "email"
#     }))
    
#     description = forms.CharField(widget = forms.Textarea(attrs={
#         "class":"form-control" ,
#         "id": "textarea"
#     }))
    
 
   
#     class Meta:
#         model = Project
#         fields = [
#             'title','specialization', 'supervisor'
#         ]
        
#         widgets = {
#             'specialization':forms.Select(attrs = {
#                 'class': "form-select",
#                 'empty_label': 'Please select Specliaization',
#                 'label': 'Select',
#                 'id': 'country',
#                 'aria-label': 'Select'
                
                
#             }),
            
#             'supervisor': forms.Select(attrs = {
#                 'class': "form-select",
#                 'empty_label': 'Please select Specliaization',
#                 'label': 'Select',
#                 'id': 'country',
#                 'aria-label': 'Select'
#         }),
            
#             'projectimg': forms.ClearableFileInput(attrs = {
#                 "class": "form-control",
#                 "id": "formFile",
#                 'label': 'Project Image (optional)'
#             })
            
#         }
        
        
#         labels = {
#             'projectimg' : 'Project Image (Optional)'
#         }
        
#         def __init__(self, *args, **kwargs):
#             super(studentRegisterForm, self).__init__(*args, **kwargs)
#             self.fields['title','supervisor']

class TaskForm(forms.ModelForm):
 
    name = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control",
      
        'placeholder': 'Please enter task name',

    }))
    
    
    
    
    
    class Meta:
        model = Task
        fields = [
            'name',
            'project',
        ]
        widgets = {
            'project':forms.Select(attrs = {
                'class': "form-select",
                'id': 'project',
                
                
            }),}
        
        labels = {
            'project' : 'Assign to project group'
        }
        
        
    def __init__(self, *args, ** kwargs):
            self.user = kwargs.pop('user', None)
            super(TaskForm, self).__init__(*args, **kwargs)
            self.fields['project'].queryset = Project.objects.filter(supervisor = self.user.supervisor)



class SpecializationForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control",
      
        'placeholder': 'Please enter task name',

    }))
    
    
    class Meta:
        model = Specialization
        fields = ['name', 'specimg']
        
        widgets = {
        'specimg': forms.ClearableFileInput(attrs = {
                "class": "form-control",
                "id": "formFile",
            })
        }
        
        labels = {
            'specimg' : 'Specialization Icon (Optional)'
        }
        
        
        
class ReportForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control",
        'placeholder': 'Please report name or title',

    }))
    class Meta:
        model = ProjectReport
        fields = ['name', 'file']
    
        widgets = {
            'file': forms.ClearableFileInput(attrs = {
                    "class": "form-control",
                    "id": "formFile",
                })
            }
            
        labels = {
            'file' : 'Select Report File (Only word and excel files allowed)'
            }
        
class ProjectFileForm(forms.ModelForm):
    filename = forms.CharField(widget = forms.TextInput(attrs = {
        "class": "form-control",
        'placeholder': 'Please report name or title',

    }))
    class Meta:
        model = ProjectFile
        fields = ['filename', 'file', 'project']
    
        widgets = {
            'file': forms.ClearableFileInput(attrs = {
                    "class": "form-control",
                    "id": "formFile",
                }),
            'project':forms.Select(attrs = {
                'class': "form-select",
                'empty_label': 'Please select Specliaization',
                'label': 'Select',
                'id': 'country',
                'aria-label': 'Select'
                
                
            }),
            }
            
        labels = {
            'file' : 'Select Report File (Only word and excel files allowed)',
            'filename': 'File Name'
            }
        
    def __init__(self, *args, ** kwargs):
            self.user = kwargs.pop('user', None)
            super(ProjectFileForm, self).__init__(*args, **kwargs)
            self.fields['project'].queryset = Project.objects.filter(supervisor = self.user.supervisor)
            
            
            
class ProfilePicForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ['studentimg']
    
        widgets  = {
        'studentimg': forms.FileInput(attrs = {
                "class": "form-control",
                "id": "formFile",
                'onchange' : "readURL(this);"
                # 'required' : False
            })
    
    }
        labels = {
            'studentimg' : False
        }
        
        
class SupervPicForm(forms.ModelForm):
    
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        ))
    
    
    other_names = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Other Names",
                "class": "form-control"
            }
        ))
    
    # email = forms.EmailField(
    #     widget=forms.EmailInput(
    #         attrs={
    #             "placeholder": "Email",
    #             "class": "form-control"
    #         }
    #     ))
    class Meta:
        model = Supervisor
        fields = ['supervisorimg', 'first_name', 'other_names']
    
        widgets  = {
        'supervisorimg': forms.FileInput(attrs = {
                "class": "form-control",
                "id": "formFile",
                # 'required' : False
            })
    
    }
        labels = {
            'supervisorimg' : False
        }