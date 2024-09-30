from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import User_details

class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    mobile_no = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mobile Number'
        }),
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Mobile number must be exactly 10 digits'
            )
        ]
    )
    collage_name = forms.CharField(
        max_length=250,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'College/Industry'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['name', 'mobile_no', 'email', 'collage_name', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Remove any unwanted fields if they exist
        if 'usable_password' in self.fields: # this is removied because default coming a radio button
            del self.fields['usable_password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['mobile_no']
        user.first_name = self.cleaned_data['name']
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password1'])  # Set the password using set_password
        user.is_active =False # need the permition from the admin to login 

        if commit:
            user.save()

        # Create User_details instance
        user_details = User_details(
            user=user,
            mobile_no=self.cleaned_data['mobile_no'],
            collage_name=self.cleaned_data['collage_name'],
        )
        if commit:
            user_details.save()
        return user
