from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard_home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('staff/', views.staff_list, name='staff_list'),  # Use staff_list view only
    path('staff/create/', views.staff_create, name='staff_create'),  # New URL
    path('staff/<int:pk>/update/', views.staff_update, name='staff_update'),
    path('<int:pk>/delete/', views.staff_delete, name='staff_delete'),

    path('subject/', views.subject_list, name='subject_list'),  # Use staff_list view only
    path('subject/create/', views.subject_create, name='subject_create'),
    path('subject/update/<int:pk>/', views.subject_update, name='subject_update'),
    path('subject/delete/<int:pk>/', views.subject_delete, name='subject_delete'),


    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/create/', views.teacher_create, name='teacher_create'),
    path('teachers/update/<int:pk>/', views.teacher_update, name='teacher_update'),
    path('teachers/delete/<int:pk>/', views.teacher_delete, name='teacher_delete'),


]