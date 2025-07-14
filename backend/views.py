from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Department, UserProfile , Subject , Teacher  # Import from models.py
from .forms import StaffCreationForm , SubjectCreationForm , TeacherForm  # Import forms
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


def subject(request):
    return render(request, 'subject/index.html')

def subject_list(request):
    subjects = Subject.objects.all().select_related('created_by', 'updated_by').order_by('id')
    return render(request, 'subject/index.html', {
        'subjects': subjects
    })

def subject_create(request):
    if request.method == 'POST':
        form = SubjectCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully!')
            return redirect('subject_list')
    else:
        form = SubjectCreationForm()
    
    return render(request, 'subject/create.html', {
        'form': form,
        'title': 'Add New Subject'
    })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from backend.models import Subject
from backend.forms import SubjectCreationForm  # Assuming you’re using the same form

def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        form = SubjectCreationForm(request.POST, instance=subject)
        if form.is_valid():
            updated_subject = form.save(commit=False)
            updated_subject.updated_by = request.user
            updated_subject.save()
            messages.success(request, 'Subject updated successfully!')
            return redirect('subject_list')
    else:
        form = SubjectCreationForm(instance=subject)

    return render(request, 'subject/update.html', {
        'form': form,
        'title': 'Update Subject',
        'subject': subject,
    })

def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)

    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('subject_list')

    return render(request, 'subject/delete.html', {
        'subject': subject
    })



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


def teacher(request):
    return render(request, 'teacher/index.html')

def teacher_list(request):
    teachers = Teacher.objects.select_related('subject', 'created_by', 'updated_by').all()
    return render(request, 'teacher/index.html', {'teachers': teachers})

def teacher_create(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.created_by = request.user
            teacher.updated_by = request.user
            teacher.save()
            messages.success(request, 'Teacher created successfully!')
            return redirect('teacher_list')
    else:
        form = TeacherForm()
    return render(request, 'teacher/create.html', {'form': form})

def teacher_update(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            updated = form.save(commit=False)
            updated.updated_by = request.user
            updated.save()
            messages.success(request, 'Teacher updated successfully!')
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'teacher/update.html', {'form': form, 'teacher': teacher})



def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'Teacher deleted successfully!')
        return redirect('teacher_list')
    return render(request, 'teacher/delete.html', {'teacher': teacher})

