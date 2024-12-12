from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User



class CustomUserCreatinForm(UserCreationForm):
    email = forms.EmailField(label="ایمیل")
    phone = forms.CharField(label="تلفن همراه",max_length=15)
    
    
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password1', 'password2')
        
        