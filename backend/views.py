from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Department, UserProfile  # Import from models.py
from .forms import StaffCreationForm
from django.contrib import messages
from django.shortcuts import redirect




def dashboard(request):
    return render(request, 'dashboard/index.html')

def staff(request):
    return render(request, 'staff/index.html')


def staff_list(request):
    staff = User.objects.all().select_related('userprofile', 'userprofile__department').order_by('id')
    return render(request, 'staff/index.html', {
        'staff': staff
    })

def staff_create(request):
    if request.method == 'POST':
        form = StaffCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff member created successfully!')
            return redirect('staff_list')
    else:
        form = StaffCreationForm()
    
    return render(request, 'staff/create.html', {
        'form': form,
        'title': 'Add New Staff'
    })

from django.shortcuts import get_object_or_404
from .forms import StaffCreationForm, StaffUpdateForm  # Add StaffUpdateForm to imports

def staff_update(request, pk):
    staff_member = get_object_or_404(User, pk=pk)
    
    # Ensure UserProfile exists
    UserProfile.objects.get_or_create(user=staff_member)
    
    if request.method == 'POST':
        form = StaffUpdateForm(request.POST, instance=staff_member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Staff member updated successfully!')
            return redirect('staff_list')
    else:
        form = StaffUpdateForm(instance=staff_member)
    
    return render(request, 'staff/update.html', {
        'form': form,
        'staff': staff_member,
        'title': f'Update {staff_member.username}'
    })

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def staff_delete(request, pk):
    staff_member = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        # Perform the deletion
        staff_member.delete()
        messages.success(request, f'Staff member {staff_member.username} has been deleted successfully!')
        return redirect('staff_list')
    
    return render(request, 'staff/delete.html', {
        'staff': staff_member
    })
