from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email= models.EmailField(max_length=100,unique=True)
    

      # Adding role field to represent the user roles
    ADMIN = 'admin'
    MANAGER = 'manager'
    USER = 'user'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (USER, 'User'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=USER,  # default role is 'User'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    

    
    def is_admin(self):
        return self.role == self.ADMIN

    def is_manager(self):
        return self.role == self.MANAGER

    def is_user(self):
        return self.role == self.USER