from celery import shared_task
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail, EmailMessage



@shared_task
def send_bulk_email(message, recipient, subject):
    mail_subject = subject
    message = message
    email = EmailMessage(
        subject = mail_subject,
        body = message,
        from_email = settings.EMAIL_HOST_USER,
        to = [recipient],
    )
    email.fail_silently = True 
    email.content_subtype = "html"  # Main content is now text/html
    email.send()
    # send_mail(
    #     subject = subject,
    #     message = body,
    #     from_email = settings.EMAIL_HOST_USER,
    #     recipient_list = [recipient],
    #     fail_silently = True
        
    # )
    
    return str( recipient)
    return 'Done'

@shared_task
def send_verification_email(subject, body,  recipient):
    email = EmailMessage(
        subject = subject,
        body = body,
        from_email = settings.EMAIL_HOST_USER,
        to = [recipient]        
    )
    email.fail_silently = True 
    
    email.content_subtype = "html"  # Main content is now text/html
    email.send()
    # send_mail(
    #     subject = subject,
    #     message = body,
    #     from_email = settings.EMAIL_HOST_USER,
    #     recipient_list = [recipient],
    #     fail_silently = True
        
    # )
    
    return str( recipient)
    

    
    
    
    # send_mail(
    #     subject = mail_subject,
    #     message = message,
    #     from_email = settings.EMAIL_HOST_USER,
    #     recipient_list = [recipient],
    #     fail_silently = True
    # )