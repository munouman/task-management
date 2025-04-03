from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponseNotFound, HttpResponseServerError
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Task, Category
from .forms import CategoryForm, NewTaskForm
from reporting.models import CompletedTask
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from accounts.decorators import manager_required, admin_required, admin_or_manager_required
from .forms import UserEditForm  
from accounts.models import CustomUser
import logging


logger = logging.getLogger(__name__)

User= get_user_model

@login_required
def index(request):
    # Tasks where the logged-in user is assigned
    todos = Task.objects.filter(completed=False, in_progress=False, users__in=[request.user]).order_by('-created_at')
    
    # Completed tasks for the logged-in user
    completed = Task.objects.filter(completed=True, users__in=[request.user]).order_by('-completed_at')[:10]
    
    # Tasks in progress for the logged-in user
    in_progress = Task.objects.filter(in_progress=True, users__in=[request.user])
    
    # Categories created by the logged-in user
    categories = Category.objects.all()
    
    # All users in the system
    users = get_user_model().objects.all()  # Get all users as a queryset
    
    context = {
        "tasks_todo": todos,
        "tasks_completed": completed,
        "tasks_in_progress": in_progress,
        "categories": categories,
        "users": users,  # Now this will be a queryset of all users
        "task_form": NewTaskForm(),
        "category_form": CategoryForm()
    }
    
    return render(request, 'dashboard/tasks_list.html', context)

@login_required
def in_progress(request, id):
    task = get_object_or_404(Task, id=id, users=request.user)
    task.in_progress = not task.in_progress
    task.save()
    return redirect('dashboard:index')


@login_required
def undo_progress(request, id):
    task = get_object_or_404(Task, id=id, users=request.user)
    task.in_progress = not task.in_progress
    task.save()
    return redirect('dashboard:index')

@login_required
def completed(request, id):
    task = get_object_or_404(Task, id=id, users=request.user)
    
    # Toggle task completion
    task.completed = not task.completed
    task.completed_at = timezone.now() if task.completed else None
    task.in_progress = False
    task.save()

    # If task is completed, create a CompletedTask
    if task.completed:
        # Assuming you want to assign the current user (request.user) to the CompletedTask
        CompletedTask.objects.create(
            title=task.title,
            created_at=task.created_at,
            completed_at=task.completed_at,
            category=task.category.name if task.category else '',
            user=request.user  # Assign the current user (request.user) here
        )

    return redirect('dashboard:index')

@login_required
def create(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Assign the logged-in user to the task
            
            # Get the selected category
            category_id = request.POST.get('category')
            category = Category.objects.filter(id=category_id, user=request.user).first()
            if not category:
                return redirect('dashboard:index')  # Handle invalid category
            
            task.category = category
            task.save()

            # Assign users to the task (many-to-many relationship)
            task.users.set(form.cleaned_data['users'])  # Assign multiple users
            task.save()

            # Add the logged-in user (assigner) to the task's users
            task.users.add(request.user)  # Ensure the task is also visible to the assigner

        return redirect('dashboard:index')
    else:
        form = NewTaskForm()

    return render(request, 'dashboard/create_task.html', {'task_form': form})

@login_required
def update(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    if request.method == 'POST':
        form = NewTaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Ensure the task user is still the logged-in user

            # Handle the category assignment
            category_id = request.POST.get('category')
            category = Category.objects.filter(id=category_id, user=request.user).first()
            if not category:
                return redirect('dashboard:index')  # Handle invalid category
            task.category = category
            task.save()

            # Update the users assigned to the task
            task.users.set(form.cleaned_data['users'])  # This updates multiple users or a single user
            task.save()

        return redirect('dashboard:index')
    else:
        form = NewTaskForm(instance=task)
    
    return render(request, 'dashboard/update_task.html', {'task_form': form})



@login_required
def delete(request, id):
    task = get_object_or_404(Task, id=id, users=request.user)
    task.delete()
    return redirect('dashboard:index')


@login_required
def reset_all(request):
    if request.method == 'POST':
        # Delete all tasks for the logged-in user
        Task.objects.filter(user=request.user).delete()
        return redirect('dashboard:index')
    return render(request, 'dashboard/confirm_reset.html')

@login_required
def new_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user  # Assuming you want to associate the category with a user
            category.save()

            # After creating the category, update the context with all categories
            categories = Category.objects.filter(user=request.user)

            # Redirect to the task creation page with the updated category list
            return redirect('dashboard:index')  # Assuming 'dashboard:create_task' is your task creation URL
        else:
            return redirect('dashboard:index')
            # return render(request, 'dashboard/create_category.html', {'category_form': form})
    else:
        form = CategoryForm()  # GET request, show an empty form
        return render(request, 'dashboard/create_category.html', {'category_form': form})

@admin_or_manager_required
# @manager_required
@staff_member_required
def clear_categories(request):
    # Clear all categories in the system (Admin-only action)
    Category.objects.all().delete()
    return redirect('dashboard:index')


def custom_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard:index')  # Redirect to dashboard after login
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


@login_required
def edit_user(request, user_id):
    user_to_edit = get_object_or_404(CustomUser, id=user_id)
    
    # Ensure only admins or the user themselves can edit
    if request.user != user_to_edit and not request.user.is_staff:
        return redirect('dashboard:user_list')

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            return redirect('dashboard:user_list')  # Redirect after save
    else:
        form = UserEditForm(instance=user_to_edit)

    return render(request, 'dashboard/edit_user.html', {'form': form, 'user': user_to_edit})

@admin_required  # Ensure only admins can access this view
@login_required
def user_list_view(request):
    users = CustomUser.objects.all()  # Fetch all users
    return render(request, 'dashboard/user_list.html', {'users': users})