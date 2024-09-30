from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class User_details(models.Model):
    user = models.OneToOneField(User,  on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to="profile_pic", blank=True, null=True)
    aadhaar_num = models.CharField(max_length=12, unique=True,blank=True, null=True)
    aadhaar_image = models.FileField(upload_to='aadhar_files/',blank=True, null=True)
    collage_name = models.CharField(max_length=250,blank=True, null=True)
    mobile_no = models.CharField(max_length=15, unique=True, default='0000000000')
    total_amount_due = models.DecimalField(max_digits=10, decimal_places=2, default=6000.00)  # Default total amount
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Amount paid by the student
    payment_status = models.BooleanField(default=False)  # True if fully paid, False otherwise

    def __str__(self):
        return f"{self.user.username} - {self.mobile_no}"

    # Method to calculate the remaining balance
    @property
    def remaining_balance(self):
        return self.total_amount_due - self.amount_paid

    # Method to update payment status
    def update_payment_status(self):
        if self.amount_paid >= self.total_amount_due:
            self.payment_status = True  # Mark as fully paid
        else:
            self.payment_status = False  # Not fully paid
        self.save()