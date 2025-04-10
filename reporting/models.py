from django.db import models
from django.contrib.auth.models import User
from dashboard.models import Category
from django.conf import settings

class CompletedTask(models.Model):
    title = models.CharField(max_length=255, default="Task")
    created_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=255, default="Others")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Completed Task"
    
    
    