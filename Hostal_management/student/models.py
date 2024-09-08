from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Payment_details(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10,decimal_places=2)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/')
    payment_date = models.DateTimeField(auto_now_add=True)  # Automatically add the payment date

    def __str__(self):
        return f'{self.user.username} - {self.amount_paid}'
    class Meta:
        ordering = ['-payment_date']  # Orders payment history by latest first