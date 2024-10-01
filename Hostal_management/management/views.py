from django.shortcuts import render, HttpResponse,redirect,get_object_or_404
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
    quaryset = User_details.objects.all()
    context = {"students":quaryset}
    return render(request,'management_panel.html',context)

def logout_page(request):
    logout(request)
    return redirect("dashboard")


def amar_profile(request):
    return render(request,'profile.html')



#################### reference the web ui https://www.infogain.com/careers/ 





def update_student(request,user_id):
    user =request.user

    user_details = get_object_or_404(User_details, id=user_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile_num = request.POST.get('mobile')
        email = request.POST.get('email')
        aadhaar_num = request.POST.get('aadhaar_num')
        college_name = request.POST.get('college_name')

        if name:
            user.first_name = name
        if mobile_num:
            user_details.mobile_num = mobile_num
            user.username = mobile_num
        if email:
            user.email = email
            # need to complete...
       
    pass