from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Enrollment
from .forms import EnrollmentForm


def enrollment_list(request):
    enrollments = Enrollment.objects.select_related('student', 'subject').order_by('-enrolled_date')
    return render(request, 'enrollments/enrollment_list.html', {'enrollments': enrollments})


def enrollment_create(request):
    form = EnrollmentForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Enrollment created!')
        return redirect('enrollment-list')
    return render(request, 'enrollments/enrollment_form.html', {'form': form, 'title': 'Add Enrollment'})


def enrollment_update(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    form = EnrollmentForm(request.POST or None, instance=enrollment)
    if form.is_valid():
        form.save()
        messages.success(request, 'Enrollment updated!')
        return redirect('enrollment-list')
    return render(request, 'enrollments/enrollment_form.html', {'form': form, 'title': 'Edit Enrollment', 'enrollment': enrollment})


def enrollment_delete(request, pk):
    enrollment = get_object_or_404(Enrollment, pk=pk)
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Enrollment deleted!')
        return redirect('enrollment-list')
    return redirect('enrollment-list')
