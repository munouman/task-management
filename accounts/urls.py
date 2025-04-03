from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),  # Name it 'signup'
    path('login/', views.login_view, name='login'),  # Name it 'login'
    path('logout/', views.logout_view, name='logout'), 
    # path('login/', auth_views.LoginView.as_view(), name='login'),
]


handler404 = 'core.views.handler404'