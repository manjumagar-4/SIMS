from django.shortcuts import render, redirect
from django.contrib import messages
from core.models import Student, Course, Subject, Faculty, Enrollment, Exam, Result
from django.db.models import Count


def login_view(request):
    if request.session.get('is_logged_in'):
        return redirect('dashboard')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        if username == 'admin' and password == 'admin':
            request.session['is_logged_in'] = True
            request.session['admin_name'] = 'Administrator'
            return redirect('dashboard')
        else:
            return render(request, 'core/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'core/login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def dashboard(request):
    if not request.session.get('is_logged_in'):
        return redirect('login')

    # KPI Stats
    total_students   = Student.objects.filter(is_active=True).count()
    total_courses    = Course.objects.filter(is_active=True).count()
    total_subjects   = Subject.objects.filter(is_active=True).count()
    total_faculty    = Faculty.objects.filter(is_active=True).count()
    total_enrollments = Enrollment.objects.filter(status='Active').count()
    total_exams      = Exam.objects.filter(is_active=True).count()
    total_results    = Result.objects.count()

    # Recent Students
    recent_students = Student.objects.select_related('course').order_by('-created_at')[:5]

    # Recent Enrollments
    recent_enrollments = Enrollment.objects.select_related('student', 'subject').order_by('-created_at')[:5]

    # Pass / Fail counts for chart
    all_results = Result.objects.all()
    pass_count = sum(1 for r in all_results if r.is_pass)
    fail_count = sum(1 for r in all_results if not r.is_pass)

    # Grade distribution
    grade_counts = {}
    for r in all_results:
        g = r.grade
        grade_counts[g] = grade_counts.get(g, 0) + 1

    # Students per course
    course_data = list(
        Course.objects.annotate(student_count=Count('students')).values('name', 'student_count')
    )

    context = {
        'total_students':    total_students,
        'total_courses':     total_courses,
        'total_subjects':    total_subjects,
        'total_faculty':     total_faculty,
        'total_enrollments': total_enrollments,
        'total_exams':       total_exams,
        'total_results':     total_results,
        'recent_students':   recent_students,
        'recent_enrollments': recent_enrollments,
        'pass_count':        pass_count,
        'fail_count':        fail_count,
        'grade_counts':      grade_counts,
        'course_data':       course_data,
    }
    return render(request, 'core/dashboard.html', context)
