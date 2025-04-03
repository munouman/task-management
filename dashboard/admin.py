from django.contrib import admin
from .models import Task, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'completed', 'in_progress', 'category', 'created_at']
    list_filter = ['completed', 'in_progress', 'category']
    search_fields = ['title', 'description']

    # Customizing the queryset to make sure only admin users can see all tasks
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs  # Admin users can see all tasks
        else:
            # For non-admin users, you can limit what they can see based on their role or tasks assigned to them
            return qs.filter(users=request.user)  # Show only tasks assigned to the current user

    # Optionally hide some fields for non-admin users
    def get_readonly_fields(self, request, obj=None):
        # Make certain fields readonly based on user type
        if not request.user.is_staff:
            return ['category']  # Example: Only admins can edit 'category'
        return []

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user']
    search_fields = ['name']

    # Customizing the queryset to make sure only admin users can see all categories
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_staff:
            return qs  # Admin users can see all categories
        else:
            return qs.filter(user=request.user)  # Non-admin users only see categories they own

    # Optionally hide certain fields for non-admin users
    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_staff:
            return ['user']  # Example: Only admins can edit 'user'
        return []

# Registering the models with the customized admin classes
admin.site.register(Task, TaskAdmin)
admin.site.register(Category, CategoryAdmin)
