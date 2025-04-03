from django.shortcuts import render , redirect 
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm,SignUpForm
from django.contrib.auth import get_user_model
from .decorators import admin_required, manager_required, user_required


users= get_user_model()

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@admin_required
@login_required  # Ensure the user is logged in before accessing this view
def signup(request):

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user to the database
            return redirect('accounts:login')  # Redirect to the login page after successful signup
    else:
        form = SignUpForm()

    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    form = LoginForm()  # Initialize the form for GET request
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard:index')  # Redirect to dashboard after login
            else:
                form.add_error(None, 'Invalid login credentials')
    else:
        # GET request: the form was already initialized above
        pass

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')  # Redirect to login after logout

