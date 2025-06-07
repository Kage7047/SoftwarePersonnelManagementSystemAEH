from django.shortcuts import render, get_object_or_404

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LeaveRequest, EmployeeProfile
from .forms import LeaveRequestForm
from django.contrib.auth import login
from .forms import UserRegisterForm

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


def is_manager(user):
    return user.is_authenticated and user.role == 'MANAGER'

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
    user = request.user
    profile = getattr(user, 'employeeprofile', None)
    return render(request, 'core/profile.html', {
        'user': user,
        'profile': profile,
    })