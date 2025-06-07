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

]
