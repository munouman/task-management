from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth.models import User
from django import forms
from .models import CustomUser
from django.contrib.auth import get_user_model

from django.contrib.auth import authenticate 
users = get_user_model()



class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required. Please provide a valid email address.')
    role = forms.ChoiceField(choices=users.ROLE_CHOICES, required=True, help_text='Select user role')

    class Meta:
        model = users
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if users.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email address already exists.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


    
class LoginForm(forms.Form):
    email= forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 rounded-lg bg-gray-700 text-gray-300 outline-none focus-within:ring-1 focus-within:ring-offset-blue-900',
            'placeholder': 'Email'
        })
)
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 rounded-lg bg-gray-700 text-gray-300 outline-none focus-within:ring-1 focus-within:ring-offset-blue-900 mb-6',
            'placeholder': 'Password'
        })
    )


        # Custom error message for failed login attempt
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")

        return cleaned_data

