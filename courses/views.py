from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Course
from .forms import CourseForm


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


def course_create(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Course created successfully!')
        return redirect('course-list')
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Add Course'})


def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        form.save()
        messages.success(request, 'Course updated successfully!')
        return redirect('course-list')
    return render(request, 'courses/course_form.html', {'form': form, 'title': 'Edit Course', 'course': course})


def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted!')
        return redirect('course-list')
    return redirect('course-list')
