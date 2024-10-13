from django.db import models
from django.contrib.auth.models import User
from student.models import PaymentDetails
from django.utils import timezone


class User_details(models.Model):
    SERVICE_CHOICES = [
        ('AF', 'Accommodation & Food'),
        ('FO', 'Food Only'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pic", blank=True, null=True)
    aadhaar_num = models.CharField(max_length=12, unique=True, blank=True, null=True)
    aadhaar_image = models.FileField(upload_to='aadhar_files/', blank=True, null=True)
    collage_name = models.CharField(max_length=250, blank=True, null=True)
    mobile_no = models.CharField(max_length=15, unique=True, default='0000000000')
    service_type = models.CharField(max_length=2, choices=SERVICE_CHOICES, default='AF')
    total_amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=6000.00)  # Default total amount
    last_payment_date = models.DateTimeField(null=True, blank=True)  # Track last payment date
    payment_status = models.BooleanField(default=False)  # True if fully paid, False otherwise

    def __str__(self):
        return f"{self.user.username} - {self.mobile_no} - {self.get_service_type_display()}"

    def save(self, *args, **kwargs):
        # Update total amount based on service type
        if self.service_type == 'AF':
            self.total_amount_due = 6000.00  # Rate for Accommodation & Food
        elif self.service_type == 'FO':
            self.total_amount_due = 3500.00  # Rate for Food Only
        super().save(*args, **kwargs)

    @property
    def remaining_balance(self):
        payments = PaymentDetails.objects.filter(user=self.user)
        total_paid = sum(payment.amount_paid for payment in payments)
        return self.total_amount_due - total_paid

    def update_payment_status(self):
        self.payment_status = self.remaining_balance <= 0  # True if fully paid
        self.save()

    def reset_remaining_balance(self):
        # Check if the last payment date is in the previous month
        if self.last_payment_date:
            last_payment_month = self.last_payment_date.month
            last_payment_year = self.last_payment_date.year
            current_month = timezone.now().month
            current_year = timezone.now().year

            if (current_month != last_payment_month or current_year != last_payment_year):
                # Reset remaining balance to the total amount due
                self.update_payment_status()  # Update the payment status accordingly
                self.save()  # Save changes to the model

        # Update last_payment_date if there are any payments
        if PaymentDetails.objects.filter(user=self.user).exists():
            self.last_payment_date = PaymentDetails.objects.filter(user=self.user).latest('payment_date').payment_date
        else:
            self.last_payment_date = None
