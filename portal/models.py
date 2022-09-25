import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


from django.contrib.auth.models import User



notification_type = (
        ('Supervisor', 'Supervisors'),
        ('Students', 'Students'),
        ('All', 'All')
    )
# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(unique=True, null = True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    indexNo = models.CharField(max_length = 255)
    studentimg = models.ImageField(upload_to='images', default ='images/superimg.png')
    project = models.ForeignKey('Project', on_delete=models.SET_NULL,related_name='projects', default = None, null = True, blank= True)
    approved = models.BooleanField(default=False)
    verified = models.BooleanField(default = False)
    def __str__(self):
        return str(self.user)
    
class Supervisor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
    email = models.EmailField(unique=True, null = True)
    rank = models.CharField(max_length=255, default = 'None')
    role =  models.CharField(max_length=255, default = 'None')
    first_name = models.CharField(max_length=255)
    other_names = models.CharField(max_length=255, null = True, blank = True)
    supervisorimg = models.ImageField(upload_to='images', default ='images/superimg.png')
    verified = models.BooleanField(default= False)
    
    
    def __str__(self):
        return (self.first_name)




# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
    specialization = models.ForeignKey('Specialization', on_delete=models.CASCADE)
    slots = models.IntegerField(default = 3)
    occupied = models.BooleanField(default = False)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add = True)
    projectimg = models.ImageField(upload_to='images', blank = True, default = 'images/project_img.png')
    projectimg2 = models.ImageField(upload_to='images', blank = True, null = True)
    projectimg3 = models.ImageField(upload_to='images', blank = True, null = True)
    
    approved = models.BooleanField(default = False)
    selected = models.BooleanField(default=False)
    def __str__(self):
        return self.title
    
class Specialization(models.Model):
    name = models.CharField(max_length=255, unique= True)
    specimg = models.ImageField(upload_to='images', default ='images/defaultspecimg.png')
    def __str__(self):
        return self.name
    
    
class ProjectFile(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, null = True, blank = True, unique= True)
    file = models.FileField(upload_to='projectfiles')
    

class Event(models.Model):
    name = models.CharField(max_length=300, unique = True)
    date = models.DateField()
  
    
    def __str__(self):
        return self.name
    
    
    
# def userFileName(instance, filename):
#     extension = filename.split('.')[-1]
#     filename = "%s.%s" % ('studentdata', extension)
#     return os.path.join('uploads', filename)

class studentData(models.Model):
    # name = models.CharField(max_length=length, ${blank=True, null=True})
    date_uploaded = models.DateTimeField(auto_now= True)
    file = models.FileField(upload_to='uploads', validators= [FileExtensionValidator(allowed_extensions=['xlsx'])])
    # migrated = models.BooleanField(default = False)


class Task(models.Model):
    name = models.CharField(max_length=255, default = 'New Task')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE, null = True)
    date_created = models.DateTimeField(auto_now= True)
    completed = models.BooleanField(default = False)
    
    def __str__(self):
        return self.project.title
    
class ProjectReport(models.Model):
    name = models.CharField(max_length=255, null= True, unique = True)
    sender = models.ForeignKey(Student, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads', validators= [FileExtensionValidator(allowed_extensions=['docs', 'docx', 'pdf', 'xlsx', 'xls', 'ppt', 'pptx'])])
    date_sent = models.DateTimeField(auto_now_add= True, null = True)
    
class Notifications(models.Model):
    sender = models.ForeignKey(User, on_delete= models.CASCADE, blank = True, null = True, related_name= 'sender')
    # msgtype = models.CharField(choices = notification_type, max_length=255, blank = True, null = True)
    receiver = models.ForeignKey(User, on_delete= models.CASCADE, blank = True, null = True, related_name='recieverS')
    message = models.TextField()
    datesent = models.DateTimeField(auto_now_add=True, blank = True, null = True)
    forcoordinator = models.BooleanField(default = False)
    read = models.BooleanField(default= False)
    
class pitchedTopic(models.Model):
    sender = models.ForeignKey(Student, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    
    
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete= models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    message = models.TextField()
    datesent = models.DateTimeField(auto_now_add=True, blank = True, null = True)
    