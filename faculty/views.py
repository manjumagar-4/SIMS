from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Faculty
from .forms import FacultyForm


def faculty_list(request):
    q = request.GET.get('q', '')
    faculty = Faculty.objects.all()
    if q:
        faculty = faculty.filter(name__icontains=q)
    return render(request, 'faculty/faculty_list.html', {'faculty_list': faculty, 'q': q})


def faculty_detail(request, pk):
    member = get_object_or_404(Faculty, pk=pk)
    subjects = member.subjects.select_related('course').all()
    return render(request, 'faculty/faculty_detail.html', {'member': member, 'subjects': subjects})


def faculty_create(request):
    form = FacultyForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Faculty member added!')
        return redirect('faculty-list')
    return render(request, 'faculty/faculty_form.html', {'form': form, 'title': 'Add Faculty'})


def faculty_update(request, pk):
    member = get_object_or_404(Faculty, pk=pk)
    form = FacultyForm(request.POST or None, instance=member)
    if form.is_valid():
        form.save()
        messages.success(request, 'Faculty updated!')
        return redirect('faculty-list')
    return render(request, 'faculty/faculty_form.html', {'form': form, 'title': 'Edit Faculty', 'member': member})


def faculty_delete(request, pk):
    member = get_object_or_404(Faculty, pk=pk)
    if request.method == 'POST':
        member.delete()
        messages.success(request, 'Faculty deleted!')
        return redirect('faculty-list')
    return redirect('faculty-list')
