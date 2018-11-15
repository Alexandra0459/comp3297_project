from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ASP.models import ClinicManager, MedicineSupply, Order, Dispatcher, Location



class SignupForm(forms.ModelForm):
    #email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = ClinicManager
        fields = ('name', 'location')

class RegisterForm(forms.ModelForm):
    class Meta:
        model = ClinicManager
        fields = ('name', 'location')