from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


User = get_user_model()

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    users = models.ManyToManyField(User)  # Many-to-many relationship with User model
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    in_progress = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        status = "Completed" if self.completed else "To do"
        return f'{self.title} | {status}'
