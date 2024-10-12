from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from  management.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from management.models import User_details
from .models import Payment_details
from django.utils import timezone
from collections import defaultdict
from django.db.models.functions import TruncMonth


#register logic 
def register(request):
    if request.method == 'POST':
        username = request.POST.get('mobile_no') # makeing the mobile number as username
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request,"User Already Exist! Try to Login")
            return redirect("login")


        
        form = UserRegistrationForm(request.POST)
        '''if form.is_valid():
    form.save()
    messages.success(request, 'Registration successful! Your account is pending approval.')
    return redirect('login')
else:
    messages.error(request, 'Please correct the errors below.')
    return render(request, 'register.html', {'form': form})
'''
        
        if form.is_valid():
        
            form.save()  # This will use set_password to hash the password
             # Custom message for waiting for admin approval
            messages.success(request, 'Registration successful! Your account is pending approval.')
            return redirect('login') 
        # else:
           
        #     messages.error(request, 'Please correct the errors below.')
    else:
        
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})





# Create your views here.
# def dashboard(request):
#     return HttpResponse("<h1>Dash_Board_student</h1>")

# student dash board after the loin 
@login_required(login_url="login")
def student_dashboard(request):
    return render(request,"student_dashboard.html")

# login_logic
def login_page(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('mobile_no')
        password = data.get('password')
        # print(username,password)  to check only

        if  not User.objects.filter(username=username).exists():
            messages.error(request,"Invalid Mobile No!!")
            return redirect('login')
        
        user = authenticate(username=username,password=password)
        if user is None:
            messages.error(request,"Invalid Password!!")
            return redirect('login')
        else:
            # print("got it") to check only
            login(request,user)
            return redirect("student_dashboard")
        
    return render(request,'login_page.html')


# update the user info
def update_user(request):
    if request.method == 'POST':
        user = request.user
        user_details = get_object_or_404(User_details, user=user)
        aadhaar_file = request.FILES.get("aadhaar_image")
        profile_img = request.FILES.get("profile_pic")
        name = request.POST.get("name")
        collage = request.POST.get("collage_name")
        aadhaar_num = request.POST.get("aadhaar_num")

        try:
            if aadhaar_num:
                user_details.aadhaar_num = aadhaar_num
            if name:
                user.first_name = name
                user.save()
            if collage:
                user_details.collage_name = collage
            if aadhaar_file:
                user_details.aadhaar_image = aadhaar_file
            if profile_img:
                user_details.profile_pic = profile_img

            user_details.save()
            messages.success(request, 'Profile updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating profile: {e}')
        
        return redirect('update_profile')

    return redirect("/student/student_dashboard/")


# update the other info. of user
@login_required
def edit_aadhaar_file(request, aadhaar_image):
    request.user.user_details.aadhaar_image = aadhaar_image
    request.user.user_details.save()
    return redirect('/student/student_dashboard/')

def logout_page(request):
    logout(request)
    return redirect("dashboard")


# add payment_details
def upload_payment(request):
    if request.method == 'POST':
        user = request.user
        # user_details = get_object_or_404(Payment_details, user=user)
        amount_paid = request.POST.get("amount_paid")
        payment_screenshot = request.FILES.get("payment_screenshot")
        if amount_paid and payment_screenshot:
            payment = Payment_details(
                user=request.user,
                amount_paid=amount_paid,
                payment_screenshot=payment_screenshot,
                payment_date=timezone.now()
            )
            payment.save()
            messages.success(request, 'Payment details uploaded successfully!')
            return redirect('payment_history')  # Redirect to a page showing the payment history
        else:
            messages.error(request, 'Please fill out all fields and upload a screenshot.')
    
    return render(request, 'upload_payment.html')

        #https://chatgpt.com/c/d3e85f8b-bde3-4577-bb1f-0bd058cfcc91

@login_required
def payment_history(request):
    # Get all payments for the logged-in user and group by month
    payments = Payment_details.objects.filter(user=request.user).annotate(
        month=TruncMonth('payment_date')  # Group by month
    ).order_by('-payment_date')

    # Group payments by month
    payments_by_month = defaultdict(list)
    for payment in payments:
        month = payment.payment_date.strftime('%B %Y')  # Format the month as "Month Year" (e.g., "August 2024")
        payments_by_month[month].append(payment)

    # Pass data to the template
    return render(request, 'payment_history.html', {'payments_by_month': payments_by_month})

