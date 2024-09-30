from django.shortcuts import render, HttpResponse,redirect
from .models import *

# Create your views here.
#this is the first viewpoint of the website
def home(request):
    return render(request, 'base.html')


"""
the login and registration were going in the student page no need to 
handel the logic for it!!

but need to write a logic for the management_login !!!!!
"""
def login_page(request):
    #login logic
    # a=1
    # if a==1:
    #     return redirect('/student')
    return render(request, 'home.html')
def amar_profile(request):
    return render(request,'profile.html')



#################### reference the web ui https://www.infogain.com/careers/ 



def all_student_details(request):
    pass

def edit_student_details(request):
    pass