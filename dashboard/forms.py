from django import forms
from .models import Task, Category
from django.contrib.auth.models import User
from accounts.models import CustomUser
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

class CategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = False  # Hide label for name field

    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control rounded-md p-1 font-light text-[#9abad8] bg-[#0d1c2a] outline-none md:w-full',
                    'placeholder': 'Add a category...',  # Placeholder for better UX
                }
            )
        }

    def clean_name(self):
        name = self.cleaned_data.get('name').strip()

        if not name:
            raise ValidationError('Category name cannot be empty.')

        # Ensure the category name length is <= 20 characters
        if len(name) > 20:
            raise ValidationError('Category name cannot be longer than 20 characters.')

        # Check if the category name already exists
        if Category.objects.filter(name__iexact=name).exists():
            raise ValidationError('A category with this name already exists.')

        return name



class NewTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = False
        self.fields['category'].label = "Task Category"
        self.fields['users'].label = "Assign Users"

        # Automatically add the current user (assigner) to the users field
        if 'initial' in kwargs and 'assigner' in kwargs['initial']:
            self.initial['users'] = kwargs['initial']['assigner']

    class Meta:
        model = Task
        fields = ['title', 'category', 'users']  # Include users, title, and category
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control rounded-md p-1 font-light text-[#9abad8] bg-[#0d1c2a] outline-none w-[93%] md:w-full',
                    'placeholder': 'Add a task...'
                }
            ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control rounded-md p-1 font-light text-[#9abad8] bg-[#0d1c2a] outline-none md:w-full',
                }
            ),
        }

    # Define the 'users' field as ModelMultipleChoiceField (for selecting multiple users)
    users = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Render as checkboxes
        required=False,  # Optional field
    )

    def clean(self):
        cleaned_data = super().clean()

        # Optional validation logic if needed
        # For example, ensure the task has at least one user assigned
        users = cleaned_data.get('users')
        if not users:
            self.add_error('users', 'At least one user must be assigned to the task.')

        return cleaned_data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'password', 'role']  # Ensure role is included

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optionally, customize field widgets for better UX
        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Leave blank if not changing'})

    # Optional: Custom field handling for password, if you're allowing password changes
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    
    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user