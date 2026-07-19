from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Exam
from .forms import ExamForm


def exam_list(request):
    exams = Exam.objects.select_related('subject__course').order_by('-exam_date')
    return render(request, 'exams/exam_list.html', {'exams': exams})


def exam_create(request):
    form = ExamForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Exam created!')
        return redirect('exam-list')
    return render(request, 'exams/exam_form.html', {'form': form, 'title': 'Schedule Exam'})


def exam_update(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    form = ExamForm(request.POST or None, instance=exam)
    if form.is_valid():
        form.save()
        messages.success(request, 'Exam updated!')
        return redirect('exam-list')
    return render(request, 'exams/exam_form.html', {'form': form, 'title': 'Edit Exam', 'exam': exam})


def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete()
        messages.success(request, 'Exam deleted!')
        return redirect('exam-list')
    return redirect('exam-list')
