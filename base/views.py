from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
# from student.models import pitchedTopic
from .decorators import *
from .forms import StudentRegistration, approveForm, PitchedForm
from portal.models import *
from coordinator.filters import *
from django.views.generic import *
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site



from coordinator.filters import *
from notifications.notifsender import *

# Create your views here.


def home(request):
    projects = Project.objects.filter(approved = True)
    specialization = Specialization.objects.all()
    supervisors = Supervisor.objects.all()
    
    
    context = {
        'specialization': specialization,
        'projects': projects,
        'supervisors': supervisors
    }
    
    
    return render(request, 'base/index.html', context)


class projectdetail(DetailView):
    model = Project
    template_name = 'base/projectdetailview.html'
    
    def get_context_data(self,**kwargs):
        context = super(projectdetail, self).get_context_data(**kwargs)
        relatedprojects = Project.objects.filter(supervisor = self.object.supervisor).distinct()
        context['related'] = relatedprojects
        return context

     


@login_required(login_url='login')
@allowed_users(allowed_roles = ['Student']) 
@verifiedstudent
@registeredstudent
def studentUpdate(request, id):
    student = request.user.student
    ins = Student.objects.get(id = student.id)
    init_data = Project.objects.get(id = id)
    subject = str(ins.last_name.title() + ' ' + ins.first_name.title() + ' selected your project')
    message = str(ins.last_name.title() + ' ' + ins.first_name.title() +  ' selected a project topic by you,  go to your dashboard to approve enrollment')
    current_site = get_current_site(request)
    email_subject = subject
    email_body = render_to_string('notifications/newprojectemail.html', {
                            'supervisorName' : init_data.supervisor,
                            'name': ins,
                            'domain': current_site,
                            'project' : init_data.title
                        })
    if init_data.occupied:
        return redirect('projectdetail', init_data.id)
    else:
        ins.project = init_data 
        ins.save()
        init_data.slots -=1
        if init_data.slots <= 0:
            init_data.occupied = True
            init_data.save()
        init_data.save()
        send_supervisor(init_data.id, request.user.id, 'Student', email_subject,  email_body, message)
        
        return redirect('studentview')

            
def all_projects(request):
    # projects = Project.objects.all()
    projects = Project.objects.filter(approved = True)
    pjectFilter = ProjectFilter(request.GET, queryset = projects)
    projects = pjectFilter.qs
    p = Paginator(projects.order_by('-date_updated'), 10)
    
    page = request.GET.get('page')
    projects = p.get_page(page)
    numb = 'a' * projects.paginator.num_pages
    specialization = Specialization.objects.all()
    supervisors = Supervisor.objects.all()
    
    
    context = {
        'specialization': specialization,
        'projects': projects,
        'supervisors': supervisors,
        'projectfilter': pjectFilter
    }
    return render(request, 'base/sortview.html', context)
def specPage(request):
    specializations = Specialization.objects.all()
    
    
    context = {
        'specializations': specializations
    }
    
    return render(request, 'base/specPage.html', context)

def category(request, cats):
    specName = Specialization.objects.get(id=cats)
    projects = Project.objects.filter(specialization = cats, approved = True)
    pjectFilter = ProjectFilter(request.GET, queryset = projects)
    projects = pjectFilter.qs
    p = Paginator(projects.order_by('-date_updated'), 10)
    page = request.GET.get('page')
    projects = p.get_page(page)
    specialization = Specialization.objects.all()
    supervisors = Supervisor.objects.all()
    
    
    context = {
        'specialization': specialization,
        'projects': projects,
        'supervisors': supervisors,
        'projectfilter': pjectFilter,
        'specName' : specName
    }
    
    return render (request, 'base/categories.html', context)


def supervisorsPage(request):
    supervisors = Supervisor.objects.all()
    supervisorFilter = SupervisorFilter(request.GET, queryset = supervisors)
    supervisors = supervisorFilter.qs 
    
    context = {
        'supervisors' : supervisors,
        'searchSupervisor': SupervisorFilter
    }
    
    return render(request, 'base/supervisorsPage.html', context)

def sortbysuperv(request, fname, onames, id):
    supervName = Supervisor.objects.get(first_name = fname, other_names = onames, id =id)
    projects = Project.objects.filter(supervisor = supervName.id, approved = True)
    pjectFilter = ProjectFilter(request.GET, queryset = projects)
    projects = pjectFilter.qs
    p = Paginator(projects.order_by('-date_updated'), 10)
    page = request.GET.get('page')
    projects = p.get_page(page)
    # specialization = Specialization.objects.all()
    # supervisors = Supervisor.objects.all()
    context = {
        # 'specialization': specialization,
        'projects': projects,
        # 'supervisors': supervisors,
        'projectfilter': pjectFilter,
        'supervName' : supervName
    }
    return render(request, 'base/bysuperv.html', context)
    
def search(request):
    searched = ''
    if request.method == 'POST':
        searched = request.POST['searched']
        projects = Project.objects.filter(title__contains=searched, approved = True)
        pjectFilter = ProjectFilter(request.GET, queryset = projects)
        projects = pjectFilter.qs
        p = Paginator(projects.order_by('-date_updated'), 10)
        page = request.GET.get('page')
        projects = p.get_page(page)
        context ={
            'searched': searched,
            'projects': projects,
            'projectfilter': pjectFilter
        }
        return render(request, 'base/portalsearch.html', context)
    else:
        projects = Project.objects.filter(title__contains=searched, approved = True)
        pjectFilter = ProjectFilter(request.GET, queryset = projects)
        projects = pjectFilter.qs
        p = Paginator(projects.order_by('-date_updated'), 10)
        page = request.GET.get('page')
        projects = p.get_page(page)
        return render(request,'base/portalsearch.html', {'projects': projects,
            'projectfilter': pjectFilter} )

@login_required(login_url='login')
@allowed_users(allowed_roles = ['Student']) 
@verifiedstudent
def PitchTopic(request):
    student = request.user.student
    form = PitchedForm(request.POST or None)
    if form.is_valid():
        pitched = pitchedTopic.objects.create(**form.cleaned_data, sender = student)
        subject = str(student.last_name.title() + ' ' + student.first_name.title() + ' pitched a project idea')
        message = str(student.last_name.title() + ' ' + student.first_name.title() + ' pitched a project idea, find the idea in pitched topics of your dashboard')
        current_site = get_current_site(request)
        email_subject = subject
        email_body = render_to_string('notifications/supapprovemail.html', {
                    'domain': current_site,
                    'name': student,
                    'project' : pitched
                })
        send_supervisors(request.user.id,'Student', message, email_subject, email_body)
        return redirect('ideasent')
        
    img_sent = "/img/illustrations/idea.png"
    context = {
        'form': form,
        'img1' : img_sent
    }
        
        
    return render(request, 'home/pitchProjectTopic.html', context)




 