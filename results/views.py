from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from core.models import Result, Student, Exam, Subject
from .forms import ResultForm
from django.db.models import Avg, Count, Max, Min


def result_list(request):
    results = Result.objects.select_related('student', 'exam__subject').order_by('-created_at')
    return render(request, 'results/result_list.html', {'results': results})


def result_detail(request, pk):
    result = get_object_or_404(Result, pk=pk)
    return render(request, 'results/result_detail.html', {'result': result})


def result_create(request):
    form = ResultForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Result recorded!')
        return redirect('result-list')
    return render(request, 'results/result_form.html', {'form': form, 'title': 'Add Result'})


def result_update(request, pk):
    result = get_object_or_404(Result, pk=pk)
    form = ResultForm(request.POST or None, instance=result)
    if form.is_valid():
        form.save()
        messages.success(request, 'Result updated!')
        return redirect('result-list')
    return render(request, 'results/result_form.html', {'form': form, 'title': 'Edit Result', 'result': result})


def result_delete(request, pk):
    result = get_object_or_404(Result, pk=pk)
    if request.method == 'POST':
        result.delete()
        messages.success(request, 'Result deleted!')
        return redirect('result-list')
    return redirect('result-list')


# ============ REPORTS ============

def result_report(request):
    """Main reports dashboard: subject-wise stats, toppers, grade distribution."""
    # All subjects that have exams with results
    subjects = Subject.objects.filter(exams__results__isnull=False).distinct()

    selected_subject_id = request.GET.get('subject')
    selected_exam_id = request.GET.get('exam')

    exams = []
    exam_results = []
    subject_stats = {}
    toppers = []

    if selected_subject_id:
        try:
            selected_subject = Subject.objects.get(pk=selected_subject_id)
            exams = Exam.objects.filter(subject=selected_subject)

            if selected_exam_id:
                try:
                    selected_exam = Exam.objects.get(pk=selected_exam_id)
                    exam_results = Result.objects.filter(
                        exam=selected_exam
                    ).select_related('student').order_by('-marks_obtained')

                    # Stats
                    all_marks = [float(r.marks_obtained) for r in exam_results if not r.is_absent]
                    pass_list = [r for r in exam_results if r.is_pass]
                    fail_list = [r for r in exam_results if not r.is_pass]

                    subject_stats = {
                        'total': exam_results.count(),
                        'pass': len(pass_list),
                        'fail': len(fail_list),
                        'avg': round(sum(all_marks) / len(all_marks), 2) if all_marks else 0,
                        'highest': max(all_marks) if all_marks else 0,
                        'lowest': min(all_marks) if all_marks else 0,
                        'pass_pct': round(len(pass_list) / exam_results.count() * 100, 1) if exam_results.count() else 0,
                    }

                    # Grade distribution
                    grade_dist = {}
                    for r in exam_results:
                        g = r.grade
                        grade_dist[g] = grade_dist.get(g, 0) + 1

                    subject_stats['grade_dist'] = grade_dist

                    # Toppers (top 5)
                    toppers = [r for r in exam_results if not r.is_absent][:5]

                except Exam.DoesNotExist:
                    pass
        except Subject.DoesNotExist:
            pass

    return render(request, 'results/result_report.html', {
        'subjects': subjects,
        'selected_subject_id': selected_subject_id,
        'selected_exam_id': selected_exam_id,
        'exams': exams,
        'exam_results': exam_results,
        'subject_stats': subject_stats,
        'toppers': toppers,
    })


def student_report(request, student_id):
    """Individual student result sheet."""
    student = get_object_or_404(Student, pk=student_id)
    results = Result.objects.filter(student=student).select_related('exam__subject').order_by('exam__subject__semester')

    # Summary stats
    total = results.count()
    passed = sum(1 for r in results if r.is_pass)
    failed = total - passed
    marks_list = [float(r.marks_obtained) for r in results if not r.is_absent]
    avg_marks = round(sum(marks_list) / len(marks_list), 2) if marks_list else 0

    return render(request, 'results/student_report.html', {
        'student': student,
        'results': results,
        'total': total,
        'passed': passed,
        'failed': failed,
        'avg_marks': avg_marks,
    })
