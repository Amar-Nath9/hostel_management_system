from django.shortcuts import render, HttpResponse,redirect,get_object_or_404
from .models import User_details,User
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
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



def update_student(request, user_id):
    # Fetch the User and User_details instances based on user_id
    user = get_object_or_404(User, id=user_id)
    user_details = get_object_or_404(User_details, user=user)

    if request.method == 'POST':
        # Fetch data from the form submission
        name = request.POST.get('name')
        mobile_num = request.POST.get('mobile')
        email = request.POST.get('email')
        aadhaar_num = request.POST.get('aadhaar_num')
        college_name = request.POST.get('college_name')
        new_password = request.POST.get('new_password')
        is_active = request.POST.get('is_active') == 'on'


        try:
            # Update User instance fields
            if name:
                user.first_name = name
            if email:
                user.email = email
            
            # Update User_details instance fields
            if mobile_num:
                user_details.mobile_no = mobile_num
                user.username = mobile_num  # Updating username with mobile number
            if aadhaar_num:
                user_details.aadhaar_num = aadhaar_num
            if college_name:
                user_details.collage_name = college_name
            # Update active status
            user.is_active = is_active

             # Only update password if a new one is provided
            if new_password:
                user.password = make_password(new_password)
                


            # Save the User and User_details instances
            user.save()
            user_details.save()

            messages.success(request, 'Profile updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating profile: {e}')
        
        # Redirect to the management dashboard after update
        return redirect('/management/') 
    
    context = {
        'user': user,
        'user_details': user_details,
    }
    
    # Fallback redirection in case of a non-POST request
    return render(request, "user_info.html",context)

       
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        
        # Optional: You might want to delete related user details
        user_details = get_object_or_404(User_details, user=user)
        user_details.delete()  # Delete the user's details

        user.delete()  # Delete the user
        messages.success(request, 'User deleted successfully.')
        return redirect('/management/')  # Redirect to the management page after deletion

    # Fallback for non-POST requests
    return redirect('/management/')