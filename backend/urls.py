from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard_home'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('staff/', views.staff_list, name='staff_list'),  # Use staff_list view only
    path('staff/create/', views.staff_create, name='staff_create'),  # New URL
    path('staff/<int:pk>/update/', views.staff_update, name='staff_update'),
    path('<int:pk>/delete/', views.staff_delete, name='staff_delete'),
]