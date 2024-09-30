from django.shortcuts import render, HttpResponse,redirect
from .models import User_details,User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
#this is the first viewpoint of the website
def home(request):
    return render(request, 'base.html')


"""
the login and registration were going in the student page no need to 
handel the logic for it!!

but need to write a logic for the management_login !!!!!
"""
# management loi logic!!
def management_login(request):

    try:
        # if already login then redirect to the man-dash
        if request.user.is_authenticated:
            return redirect('/management/')

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.info(request,"This login is for the admin !!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user_obj = authenticate(username=username, password=password)

            if user_obj and user_obj.is_superuser:
                login(request,user_obj)
                return redirect('/management/')
            
            messages.info(request,"Invalid Password")
            return redirect('/')
        return render(request,"admin_login.html")

    except Exception as e:
        print(e)

#mangement panel
@login_required(login_url="/management-login/")
def management_dashboard(request):
    return render(request,'management_panel.html')

def logout_page(request):
    logout(request)
    return redirect("dashboard")


def amar_profile(request):
    return render(request,'profile.html')



#################### reference the web ui https://www.infogain.com/careers/ 



def all_student_details(request):
    pass

def edit_student_details(request):
    pass