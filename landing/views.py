from django.shortcuts import render

# Create your views here.
def homeindex(request):
    
    
    return render(request, 'landing/index.html')