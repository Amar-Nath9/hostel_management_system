from django.shortcuts import render,HttpResponse,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from  management.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        username = request.POST.get('mobile_no')
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request,"User Already Exist! Try to Login")
            return redirect("register")


        
        form = UserRegistrationForm(request.POST)
        
        
        if form.is_valid():
        
            form.save()  # This will use set_password to hash the password
            messages.success(request, 'Your account has been created successfully! You can now log in.')
            return redirect('login')  # Redirect to the login page or any other page of your choice
        # else:
           
        #     messages.error(request, 'Please correct the errors below.')
    else:
        
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})





# Create your views here.
def dashboard(request):
    return HttpResponse("<h1>Dash_Board_student</h1>")


@login_required(login_url="login")
def student_dashboard(request):
    return render(request,"student_dashboard.html")


def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('mobile_no')
        password = data.get('password')
        print(username,password)

        if  not User.objects.filter(username=username).exists():
            messages.error(request,"Invalid Mobile No!!")
            return redirect('login')
        
        user = authenticate(username=username,password=password)
        if user is None:
            messages.error(request,"Invalid Password!!")
            return redirect('login')
        else:
            print("got it")
            login(request,user)
            return redirect("student_dashboard")
        
    return render(request,'login_page.html')

def update_user(request,id):
    print(id)# need to update this update model
    return redirect("/student/student_dashboard/")


def logout_page(request):
    logout(request)
    return redirect("dashboard")