from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from .models import CustomUser

# Define a custom admin class for CustomUser model
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('email', 'username')
    ordering = ('email',)

    # Add fields to be displayed in the user change form
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'role')}),  # Include role here
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Add fields to be displayed in the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_active', 'is_staff')  # Include role
        }),
    )

# Register CustomUser with the admin panel
admin.site.register(CustomUser, CustomUserAdmin)

# Define a custom admin class for the Group model
class CustomGroupAdmin(GroupAdmin):
    list_display = ('name', 'get_permissions')
    search_fields = ('name',)
    ordering = ('name',)

    # Add a custom method to display the permissions of each group
    def get_permissions(self, obj):
        return ", ".join([perm.name for perm in obj.permissions.all()])
    get_permissions.short_description = 'Permissions'  # Title for the custom column

# Register Group model with the custom GroupAdmin class
admin.site.unregister(Group)  # Unregister the default Group admin
admin.site.register(Group, CustomGroupAdmin)  # Register with the custom admin class
