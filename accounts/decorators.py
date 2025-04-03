from django.http import HttpResponseForbidden
from functools import wraps
from django.contrib.auth import get_user_model

User = get_user_model()

from django.shortcuts import redirect

from django.http import HttpResponseForbidden
from django.shortcuts import redirect

def admin_or_manager_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated
        
        # Check if the user is a superuser or has the 'manager' role
        if not (request.user.is_superuser or request.user.role == 'manager'):
            return HttpResponseForbidden("You do not have permission to access this page.")
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    """
    Decorator to ensure the user is either a superuser or has the admin role.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and either a superuser or has the 'admin' role
        if request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'admin'):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to view this page.")
    return _wrapped_view

def manager_required(view_func):
    """
    Decorator to ensure the user is a manager.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Ensure the user is authenticated and has the 'manager' role
        if request.user.is_authenticated and request.user.groups.filter(name='Manager').exists():
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to view this page.")
    return _wrapped_view

def user_required(view_func):
    """
    Decorator to ensure the user is a regular user.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'user':
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden("You do not have permission to view this page.")
    return _wrapped_view
