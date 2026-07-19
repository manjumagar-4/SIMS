from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Subject
from .forms import SubjectForm


def subject_list(request):
    subjects = Subject.objects.select_related('course', 'faculty').all()
    return render(request, 'subjects/subject_list.html', {'subjects': subjects})


def subject_create(request):
    form = SubjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Subject created!')
        return redirect('subject-list')
    return render(request, 'subjects/subject_form.html', {'form': form, 'title': 'Add Subject'})


def subject_update(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(request.POST or None, instance=subject)
    if form.is_valid():
        form.save()
        messages.success(request, 'Subject updated!')
        return redirect('subject-list')
    return render(request, 'subjects/subject_form.html', {'form': form, 'title': 'Edit Subject', 'subject': subject})


def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted!')
        return redirect('subject-list')
    return redirect('subject-list')
