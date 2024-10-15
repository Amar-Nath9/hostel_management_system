from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from  management.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from management.models import User_details
from .models import PaymentDetails
from django.utils import timezone
from collections import defaultdict
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from django.db.models import Sum
from datetime import datetime
from django.utils.timezone import make_aware


# register logic 
def register(request):
    if request.method == 'POST':
        username = request.POST.get('mobile_no')  # Making the mobile number as username
        user = User.objects.filter(username=username)
        
        if user.exists():
            messages.info(request, "User Already Exist! Try to Login")
            return redirect("login")

        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            form.save()  # This will use set_password to hash the password
            
            # Custom message for waiting for admin approval
            messages.success(request, 'Registration successful! Your account is pending approval.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})




# Create your views here.
# def dashboard(request):
#     return HttpResponse("<h1>Dash_Board_student</h1>")

# student dash board after the loin 
# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, get_object_or_404
# from django.db.models import Sum
# from management.models import User_details
# from student.models import PaymentDetails
@login_required(login_url="login")
def student_dashboard(request):
    user_details = get_object_or_404(User_details, user=request.user)
    
    # Reset remaining balance if needed
    user_details.reset_remaining_balance()
    
    # Get the current month and year
    current_month = now().month
    current_year = now().year
    
    # Filter for payments in the current month
    current_month_payments = PaymentDetails.objects.filter(
        user=request.user,
        payment_date__year=current_year,
        payment_date__month=current_month
    )
    
    # Calculate total amount paid for the current month
    total_paid_current_month = current_month_payments.aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0
    remaining_balance_current_month = user_details.total_amount_due - total_paid_current_month
    
    # Retrieve all payment history for the user
    all_payments = PaymentDetails.objects.filter(user=request.user).order_by('-payment_date')
    
    # Context data to pass to the template
    context = {
        'user_details': user_details,
        'total_paid': total_paid_current_month,
        'remaining_balance': remaining_balance_current_month,
        'payments': current_month_payments,  # For current month history
        'all_payments': all_payments,  # For all payment history
    }
    
    return render(request, 'student_dashboard.html', context)

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

@login_required
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

@login_required
def upload_payment(request):
    if request.method == 'POST':
        user = request.user
        amount_paid = request.POST.get("amount_paid")
        payment_date_str = request.POST.get("payment_date")
        payment_screenshot = request.FILES.get("payment_screenshot")

        # Parse the payment date from the form
        try:
            payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d')
            payment_date = make_aware(payment_date)  # Ensure date is timezone aware

            # Check if the student has already made a payment for the specified month
            existing_payment = PaymentDetails.objects.filter(
                user=user,
                payment_date__year=payment_date.year,
                payment_date__month=payment_date.month
            ).first()

            if existing_payment:
                messages.error(request, 'You have already made a payment for this month.')
                return redirect('student_dashboard')

            # Check if amount and screenshot are provided
            if amount_paid and payment_screenshot:
                payment = PaymentDetails(
                    user=user,
                    amount_paid=float(amount_paid),
                    payment_screenshot=payment_screenshot,
                    payment_date=payment_date  # Use specified date
                )
                payment.save()

                # Update payment status in User_details
                user_details = get_object_or_404(User_details, user=user)
                user_details.update_payment_status()  # Update payment status based on new payments

                messages.success(request, 'Payment details uploaded successfully!')
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Please fill out all fields and upload a screenshot.')

        except ValueError:
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
        except Exception as e:
            messages.error(request, f'Error adding payment: {e}')

    return redirect('student_dashboard')