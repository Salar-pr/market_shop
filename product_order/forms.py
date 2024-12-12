from .models import UserProfile
from django import forms


class AddItem(forms.Form):
    product_id = forms.IntegerField()
    color_id = forms.IntegerField()
    count = forms.IntegerField()


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 
            'address', 'city', 'postcode', 'card_number'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'نام خانوادگی'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'آدرس ایمیل'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره تلفن'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'آدرس '}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شهر'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد پستی'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'شماره کارت '}),
        }
