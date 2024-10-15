from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from .models import User_details, User
from student.models import PaymentDetails  # Import the PaymentDetails model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.utils.timezone import make_aware
from datetime import datetime
from django.contrib.auth.decorators import login_required

# Home view
def home(request):
    return render(request, 'base.html')

# Management login
def management_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('/management/')

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.info(request, "This login is for the admin !!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user_obj = authenticate(username=username, password=password)

            if user_obj and user_obj.is_superuser:
                login(request, user_obj)
                return redirect('/management/')
            
            messages.info(request, "Invalid Password")
            return redirect('/')
        return render(request, "admin_login.html")

    except Exception as e:
        print(e)

# Management dashboard
@login_required(login_url="/management-login/")
def management_dashboard(request):
    queryset = User_details.objects.all()
    context = {"students": queryset}
    return render(request, 'management_panel.html', context)

# Logout
def logout_page(request):
    logout(request)
    return redirect("dashboard")

# Profile view Developer 
def amar_profile(request):
    return render(request, 'profile.html')

# Update student and add payment history
@login_required
def update_student(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user_details = get_object_or_404(User_details, user=user)

    if request.method == 'POST':
        name = request.POST.get('name')
        mobile_num = request.POST.get('mobile')
        email = request.POST.get('email')
        aadhaar_num = request.POST.get('aadhaar_num')
        college_name = request.POST.get('college_name')
        new_password = request.POST.get('new_password')
        service_type = request.POST.get('service_type')
        is_active = request.POST.get('is_active') == 'on'

        try:
            if name:
                user.first_name = name
            if email:
                user.email = email
            if mobile_num:
                user_details.mobile_no = mobile_num
                user.username = mobile_num  # Updating username with mobile number
            if aadhaar_num:
                user_details.aadhaar_num = aadhaar_num
            if college_name:
                user_details.collage_name = college_name
            if service_type:  # Update service type
                user_details.service_type = service_type
            user.is_active = is_active

            if new_password:
                user.password = make_password(new_password)
                
            user.save()
            user_details.save()

            messages.success(request, 'Profile updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating profile: {e}')
        
        return redirect('/management/') 
    
    # Retrieve payment history for the user
    payment_history = PaymentDetails.objects.filter(user=user).order_by('-payment_date')

    context = {
        'user': user,
        'user_details': user_details,
        'payment_history': payment_history,
    }
    return render(request, "user_info.html", context)

# Add payment for a student
@login_required
def add_payment(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        amount_paid = request.POST.get('amount_paid')
        payment_date_str = request.POST.get('payment_date')

        # Parse the date from the form
        try:
            payment_date = datetime.strptime(payment_date_str, '%Y-%m-%d')
            payment_date = make_aware(payment_date)  # Make the date timezone aware

            # Create the payment record
            payment = PaymentDetails(
                user=user,
                amount_paid=amount_paid,
                payment_date=payment_date,
                is_approved=False  # Default to unapproved
            )
            payment.save()
            messages.success(request, 'Payment added successfully. Awaiting approval.')
        except ValueError:
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')

        except Exception as e:
            messages.error(request, f'Error adding payment: {e}')
        
        return redirect('update_student', user.id)

    return redirect('update_student', user.id)


#payment Approvel
@login_required
def approve_payment(request, payment_id):
    payment = get_object_or_404(PaymentDetails, id=payment_id)

    if request.method == 'POST':
        payment.is_approved = True
        payment.save()
        messages.success(request, 'Payment approved successfully.')

    return redirect('update_student', payment.user.id)

@login_required
def disapprove_payment(request, payment_id):
    payment = get_object_or_404(PaymentDetails, id=payment_id)

    if request.method == 'POST':
        # For approved payments, revert the approval status
        if payment.is_approved:
            payment.is_approved = False
            payment.save()
            messages.success(request, 'Payment disapproved successfully.')
        else:
            # For unapproved payments, delete the payment record
            payment.delete()
            messages.success(request, 'Payment removed successfully.')

    return redirect('update_student', payment.user.id)
# Delete user
@login_required    
def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user_details = get_object_or_404(User_details, user=user)
        user_details.delete()
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('/management/')
    return redirect('/management/')
