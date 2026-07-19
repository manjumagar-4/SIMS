from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Student
from .forms import StudentForm


def student_list(request):
    q = request.GET.get('q', '')
    students = Student.objects.select_related('course').order_by('student_id')
    if q:
        students = students.filter(
            first_name__icontains=q
        ) | students.filter(last_name__icontains=q) | students.filter(student_id__icontains=q)
    return render(request, 'students/student_list.html', {'students': students, 'q': q})


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    enrollments = student.enrollments.select_related('subject').all()
    results = student.results.select_related('exam__subject').order_by('-exam__exam_date')
    return render(request, 'students/student_detail.html', {
        'student': student, 'enrollments': enrollments, 'results': results
    })


def student_create(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student created successfully!')
        return redirect('student-list')
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Add Student'})


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('student-detail', pk=pk)
    return render(request, 'students/student_form.html', {'form': form, 'title': 'Edit Student', 'student': student})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, 'Student deleted successfully!')
        return redirect('student-list')
    return redirect('student-list')
