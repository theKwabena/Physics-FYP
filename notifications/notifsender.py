from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import User
from portal.models import *
from django.core.mail import send_mail
from .tasks import send_bulk_email as send_emails




def send_general(room, sender,message, subject, email_body):
    # sender = request.user.supervisor
    if room == 'general':
        img = Supervisor.objects.get(user=sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room,
            {   
                'type': 'send_notifications',
                'notiftype': 'Supervisor',
                'sender' : str(sender),
                'senderimg': str(img.supervisorimg.url),
                'message': message,
            }  
        )
        for user in User.objects.all():
            if user.id != sender:
                Notifications.objects.create(sender =User.objects.get(id=sender), receiver = user, message = message)
                send_emails.delay(email_body, user.email, subject)  
            else:
                pass  
     
    elif room == 'supervisors':
        img = Supervisor.objects.get(user=sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room,
            {   
                'type': 'send_notifications',
                'notiftype': 'Supervisor',
                'sender' : str(sender),
                'senderimg': str(img.supervisorimg.url),
                'message': message,
            }  
        )
        for supervisor in Supervisor.objects.all():
            if Supervisor.user.id != sender:
                Notifications.objects.create(sender =User.objects.get(id=sender), receiver = supervisor.user, message = message)
                send_emails.delay(email_body, supervisor.email, subject)
            else:
                pass
             
    elif room == 'students':
        img = Supervisor.objects.get(user=sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            room,
            {   
                'type': 'send_notifications',
                'notiftype': 'Student',
                'sender' : str(sender),
                'senderimg': str(img.supervisorimg.url),
                'message': message,
            }  
        )
        for student in Student.objects.all():
            Notifications.objects.create(sender =User.objects.get(id=sender), receiver = student.user, message = message)
            send_emails.delay(email_body, student.email, subject)
            
            
    
def send_coordinator(sender,sender_type, receiver, message, subject, email_body):
    if sender_type == 'Student':
        img = Student.objects.get(user = sender)
        receiver = Supervisor.objects.get(id = receiver.id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'coordinator',
            {   
            'type': 'send_notifications',
            'notiftype': 'Student',
            'sender' : str(sender),
            'senderimg': str(img.studentimg.url),
            'message': message,
                }  
                    )
    elif sender_type == 'Supervisor':
        img = Supervisor.objects.get(user = sender)
        receiver = Supervisor.objects.get(id = receiver.id)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'coordinator',
            {   
            'type': 'send_notifications',
            'notiftype': 'Supervisor',
            'sender' : str(sender),
            'senderimg': str(img.supervisorimg.url),
            'message': message,
                }  
                )
        
    receiver = Supervisor.objects.get(id = receiver.id )
    Notifications.objects.create(sender=User.objects.get(id=sender), receiver = receiver.user, message = message, forcoordinator = True)
    send_emails.delay(email_body,receiver.email,subject)
    

def send_supervisor(project_id, sender, sender_type , subject, email_body, message):
    project = Project.objects.get(id = project_id)
    if sender_type == 'Coordinator':
        img = Supervisor.objects.get(user = sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'supervisor'+ str(project.supervisor.id),
            {   
            'type': 'send_notifications',
            'notiftype': 'Supervisor',
            'sender' : str(sender),
            'senderimg': str(img.supervisorimg.url),
            'message': message,
                }  
                )
    
    elif sender_type == 'Student':
        img = Student.objects.get(user = sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'supervisor'+ str(project.supervisor.id),
            {   
            'type': 'send_notifications',
            'notiftype': 'Student',
            'sender' : str(sender),
            'senderimg': str(img.studentimg.url),
            'message': message,
                }  
                )
    receiver = Supervisor.objects.get(id = project.supervisor.id)
    Notifications.objects.create(sender=User.objects.get(id=sender), receiver = receiver.user, message = message)
    send_emails.delay(email_body,receiver.email,subject)
    
    
    
def send_student(sender, sender_type,message, student_id,  subject, email_body):
    if sender_type == 'Supervisor' or sender_type == 'Coordinator':
        img = Supervisor.objects.get(user=sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'student'+str(student_id),
            {   
                'type': 'send_notifications',
                'notiftype': 'Supervisor',
                'sender' : str(sender),
                'senderimg': str(img.supervisorimg.url),
                'message': message,
            }  
        )
        
        
    elif sender_type == 'Student':
        img = Student.objects.get(user=sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'student'+str(student_id),
            {   
                'type': 'send_notifications',
                'notiftype': 'Supervisor',
                'sender' : str(sender),
                'senderimg': str(img.studentimg.url),
                'message': message,
            }  
        )
    receiver = Student.objects.get(id = student_id)
    Notifications.objects.create(sender=User.objects.get(id=sender), receiver = receiver.user, message = message)
    send_emails.delay(email_body,receiver.email,subject)
    
    
    
def send_project_group(sender, sender_type, message, project_id):
    project = Project.objects.get(id= project_id)
    if sender_type == 'Supervisor' or sender_type == 'Coordinator':
        img = Supervisor.objects.get(user=sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'project'+str(project_id),
            {   
                'type': 'send_notifications',
                'notiftype': 'Supervisor',
                'sender' : str(sender),
                'senderimg': str(img.supervisorimg.url),
                'message': message,
            }  
        )
        
        
    elif sender_type == 'Student':
        img = Student.objects.get(user=sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'project'+str(project_id),
            {   
                'type': 'send_notifications',
                'notiftype': 'Supervisor',
                'sender' : str(sender),
                'senderimg': str(img.studentimg.url),
                'message': message,
            }  
        )
    for student in Student.objects.filter(project_id =project.id):
        Notifications.objects.create(sender=User.objects.get(id=sender), receiver = student.user, message = message)
        send_emails.delay(message,student.email )
   
   
   
#    elif room == 'coordinator':
#         if sender_type == 'Student':
#             img = Student.objects.get(user=sender)
#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.group_send)(
#                 room,
#                 {   
#                     'type': 'send_notifications',
#                     'stype': 'Student',
#                     'sender' : str(sender),
#                     'senderimg': str(img.studentimg.url),
#                     'message': message,
#                 }  
#         )
#         elif sender_type == 'Supervisor':
#             img = Supervisor.objects.get(user=sender)
#             channel_layer = get_channel_layer()
#             async_to_sync(channel_layer.group_send)(
#                 room,
#                 {   
#                     'type': 'send_notifications',
#                     'stype': 'Supervisor',
#                     'sender' : str(sender),
#                     'senderimg': str(img.supervisorimg.url),
#                     'message': message,
#                 }  
#         )  
#         receiver = Supervisor.objects.get(isCoordinator = True)
#         Notifications.objects.create(sender=User.objects.get(id=sender), receiver = receiver.user, message = message)
#         send_emails.delay(message,receiver.email )


def send_supervisors(sender, sender_type, message,  subject, email_body):
    if sender_type == 'Supervisor' or sender_type == 'Coordinator':
        img = Supervisor.objects.get(user=sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'supervisors',
            {   
                'type': 'send_notifications',
                'notiftype': 'Supervisor',
                'sender' : str(sender),
                'senderimg': str(img.supervisorimg.url),
                'message': message,
            }  
        )
        
        
    elif sender_type == 'Student':
        img = Student.objects.get(user=sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'supervisors',
            {   
                'type': 'send_notifications',
                'notiftype': 'Student',
                'sender' : str(sender),
                'senderimg': str(img.studentimg.url),
                'message': message,
            }  
        )
    # receiver = Student.objects.get(id = student_id)
    for supervisor in Supervisor.objects.all():
        Notifications.objects.create(sender=User.objects.get(id=sender), receiver = supervisor.user, message = message)
        send_emails.delay(email_body,supervisor.email,subject)
        
        
        
        
def send_codPersonal(sender, sender_type,message, supervisor_id,  subject, email_body):
    if sender_type == 'Supervisor' or sender_type == 'Coordinator':
        img = Supervisor.objects.get(user=sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'supervisor'+str(supervisor_id),
            {   
                'type': 'send_notifications',
                'notiftype': 'Supervisor',
                'sender' : str(sender),
                'senderimg': str(img.supervisorimg.url),
                'message': message,
            }  
        )
        
        
    elif sender_type == 'Student':
        img = Student.objects.get(user=sender)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'supervisor'+str(supervisor_id),
            {   
                'type': 'send_notifications',
                'notiftype': 'Supervisor',
                'sender' : str(sender),
                'senderimg': str(img.studentimg.url),
                'message': message,
            }  
        )
    receiver = Supervisor.objects.get(id = supervisor_id)
    Notifications.objects.create(sender=User.objects.get(id=sender), receiver = receiver.user, message = message, forcoordinator = True)
    send_emails.delay(email_body,receiver.email,subject)
    