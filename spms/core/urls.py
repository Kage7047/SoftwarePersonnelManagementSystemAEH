from django.urls import path
from . import views

urlpatterns = [
    path('leave/apply/', views.create_leave_request, name='apply_leave'),
    path('leave/my/', views.view_my_leaves, name='my_leaves'),
    path('leave/pending/', views.pending_leave_requests, name='pending_leaves'),
    path('leave/approve/<int:leave_id>/', views.approve_leave, name='approve_leave'),
    path('leave/reject/<int:leave_id>/', views.reject_leave, name='reject_leave'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('tasks/assign/', views.assign_task, name='assign_task'),
    path('tasks/', views.task_list, name='task_list'),
    path('task/<int:task_id>/complete/', views.mark_task_complete, name='mark_task_complete'),
   # path('admin/security/safety-report/', views.view_safety_report, name='view_safety_report'),
   # path('admin/security/pip-audit/', views.pip_audit_view, name='pip_audit'),
]
