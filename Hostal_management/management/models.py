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

   