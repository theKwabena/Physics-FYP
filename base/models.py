# from django.db import models
# from django.contrib.auth.models import User


# # Create your models here.
# class Student(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     indexNo = models.CharField(max_length = 255)
#     studentimg = models.ImageField(upload_to='images', default ='images/project_img.png')
#     project = models.ForeignKey('Project', on_delete=models.CASCADE,related_name='projects', default = None, null = True, blank= True)
    
#     def __str__(self):
#         return str(self.user)
    
# class Supervisor(models.Model):
#     choices = (
#         (1, 'MR'),
#         (2, 'DR'),
#         (3, 'PROF')
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null = True, blank = True)
#     title = models.CharField(max_length=255, blank = True, null = True, choices = choices)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255, null = True, blank = True)
#     specimg = models.ImageField(upload_to='images', default ='images/project_img.png')
#     bio = models.CharField(max_length = 600,default = 'Physics Lecturer')
    
    
#     def __str__(self):
#         return str(self.f_name + ' ' + self.s_name)




# # Create your models here.

# class Project(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()
#     supervisor = models.ForeignKey(Supervisor, on_delete=models.CASCADE)
#     specialization = models.ForeignKey('Specialization', on_delete=models.CASCADE)
#     slots = models.IntegerField(default = 3)
#     date_updated = models.DateTimeField(auto_now=True)
#     date_created = models.DateTimeField(auto_now_add = True)
#     projectimg = models.ImageField(upload_to='images', blank = True, default = 'images/project_img.png')
#     approved = models.BooleanField(default = False)
#     def __str__(self):
#         return self.title
    
# class Specialization(models.Model):
#     name =models.CharField(max_length=255)
#     specimg = models.ImageField(upload_to='images', default ='images/project_img.png')
#     def __str__(self):
#         return self.name
    
    
# class ProjectFile(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     filename = models.CharField(max_length=255, null = True, blank = True)
#     file = models.FileField(upload_to='projectfiles')
    