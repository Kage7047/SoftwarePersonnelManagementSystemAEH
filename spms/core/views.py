from django.shortcuts import render, get_object_or_404

from .models import LeaveRequest, EmployeeProfile
from .forms import LeaveRequestForm
from django.contrib.auth import login
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def is_manager(user):
    return user.is_authenticated and user.role == 'MANAGER'

def is_manager_or_hr(user):
    return user.is_authenticated and user.role in ['MANAGER', 'HR']

@login_required
@user_passes_test(is_manager_or_hr)
def assign_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.assigned_by = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'core/assign_task.html', {'form': form})

@login_required
def task_list(request):
    if request.user.role == 'EMPLOYEE':
        tasks = Task.objects.filter(assigned_to=request.user)
    elif request.user.role in ['MANAGER']:
        tasks = Task.objects.filter(assigned_by=request.user)
    else:
        tasks = Task.objects.all()
    return render(request, 'core/task_list.html', {'tasks': tasks})

@login_required
def create_leave_request(request):
    user = request.user
    try:
        profile = user.employeeprofile
    except EmployeeProfile.DoesNotExist:
        return render(request, 'core/error.html', {'message': 'Profile not found'})

    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = profile
            leave.save()
            return redirect('my_leaves')
    else:
        form = LeaveRequestForm()

    return render(request, 'core/leave_form.html', {'form': form})

@login_required
def view_my_leaves(request):
    profile = request.user.employeeprofile
    leaves = LeaveRequest.objects.filter(employee=profile)
    return render(request, 'core/my_leaves.html', {'leaves': leaves})

@user_passes_test(is_manager)
def review_leave_requests(request):
    pending_requests = LeaveRequest.objects.filter(status='PENDING')
    return render(request, 'core/review_leaves.html', {'leaves': pending_requests})

@user_passes_test(is_manager)
def update_leave_status(request, leave_id, status):
    leave = LeaveRequest.objects.get(id=leave_id)
    if status in ['APPROVED', 'REJECTED']:
        leave.status = status
        leave.save()
    return redirect('review_leaves')

@login_required
def pending_leave_requests(request):
    if request.user.role != 'MANAGER' and not request.user.is_superuser:
        return render(request, 'core/error.html', {'message': 'Access denied'})

    pending = LeaveRequest.objects.filter(status='PENDING')
    return render(request, 'core/pending_leaves.html', {'requests': pending})

@login_required
def approve_leave(request, leave_id):
    if request.user.role != 'MANAGER' and not request.user.is_superuser:
        return render(request, 'core/error.html', {'message': 'Access denied'})

    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = 'APPROVED'
    leave.save()
    return redirect('pending_leaves')

@login_required
def reject_leave(request, leave_id):
    if request.user.role != 'MANAGER' and not request.user.is_superuser:
        return render(request, 'core/error.html', {'message': 'Access denied'})

    leave = get_object_or_404(LeaveRequest, id=leave_id)
    leave.status = 'REJECTED'
    leave.save()
    return redirect('pending_leaves')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            print("Form is valid")
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.save()

            EmployeeProfile.objects.create(
                user=user,
                department=form.cleaned_data['department'],
                salary=form.cleaned_data['salary'],
            )

            login(request, user)
            return redirect('profile')
        else:
            print("Form errors:", form.errors)
    else:
        form = UserRegisterForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def profile(request):
    profile = None
    all_profiles = None

    try:
        profile = EmployeeProfile.objects.get(user=request.user)
    except EmployeeProfile.DoesNotExist:
        pass  # Profile will remain None

    if request.user.role == 'HR':
        all_profiles = EmployeeProfile.objects.select_related('user')

    return render(request, 'core/profile.html', {
        'profile': profile,
        'all_profiles': all_profiles,
    })

@login_required
def mark_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Ensure only the assigned user or maybe manager can mark complete
    if request.user == task.assigned_to or request.user.role == 'MANAGER':
        task.status = 'COMPLETED'
        task.save()
    else:
        # Optionally, handle unauthorized access (return error or redirect)
        return render(request, 'core/error.html', {'message': 'Access denied'})

    return redirect('task_list')