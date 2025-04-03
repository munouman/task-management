# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.admin.views.decorators import staff_member_required
# from .models import CompletedTask
# from django.utils import timezone

# @login_required
# def tasks_history(request):
#     # Get Tasks completed
#     completed = CompletedTask.objects.filter(user=request.user).order_by('-completed_at')
#     context = {
#         "page": completed,
#     }
#     return render(request, 'reporting/tasks_history.html', context)

# @staff_member_required
# def clear_history(request):
#     CompletedTask.objects.all().delete()
#     return redirect('reporting:tasks_history')









from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import CompletedTask
from django.utils import timezone
from django.core.paginator import Paginator

@login_required
def tasks_history(request):
    # Get Tasks completed by the logged-in user
    completed = CompletedTask.objects.filter(user=request.user).order_by('-completed_at')
    
    # Pagination
    paginator = Paginator(completed, 8)  # Show 10 tasks per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, 'reporting/tasks_history.html', context)

@staff_member_required
def clear_history(request):
    timestamp = timezone.now()  # Log the time of clearing
    CompletedTask.objects.all().delete()
    messages.success(request, f"All completed tasks have been cleared successfully at {timestamp}.")
    return redirect('reporting:tasks_history')
