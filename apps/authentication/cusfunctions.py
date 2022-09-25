from django.contrib.auth.models import User



def generate_username(first_name, other_names):
    counter = 1
    username = ''
    last_names = other_names.split(' ')
    if len(last_names) == 2:
        username = first_name[0].lower() + last_names[0][0].lower() + last_names[1].lower()
    elif len(last_names) == 3:
        username = first_name[0].lower() + last_names[0][0].lower() + last_names[-1].lower
    else:
        username = first_name[0].lower() + last_names[-1].lower()
        
    while User.objects.filter(username=username):
        generated = username + str(counter)
        counter += 1
        username = generated
    return username