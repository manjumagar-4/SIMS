from django.contrib import admin
from core.models import Faculty, Course, Subject, Student, Enrollment, Exam, Result


@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'name', 'department', 'designation', 'email', 'is_active')
    search_fields = ('name', 'employee_id', 'email', 'department')
    list_filter = ('designation', 'department', 'is_active')
    ordering = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'duration_years', 'total_semesters', 'is_active')
    search_fields = ('name', 'code')
    list_filter = ('duration_years', 'is_active')
    ordering = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'course', 'faculty', 'semester', 'credit_hours', 'subject_type')
    search_fields = ('name', 'code')
    list_filter = ('course', 'semester', 'subject_type', 'is_active')
    ordering = ('course', 'semester', 'name')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'email', 'course', 'current_semester', 'status')
    search_fields = ('student_id', 'first_name', 'last_name', 'email')
    list_filter = ('course', 'status', 'gender', 'enrollment_year')
    ordering = ('student_id',)

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Full Name'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'enrolled_date', 'status')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name')
    list_filter = ('status', 'enrolled_date')
    ordering = ('-enrolled_date',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'exam_type', 'exam_date', 'max_marks', 'pass_marks', 'academic_year')
    search_fields = ('name', 'subject__name', 'academic_year')
    list_filter = ('exam_type', 'academic_year', 'is_active')
    ordering = ('-exam_date',)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'marks_obtained', 'is_absent', 'created_at')
    search_fields = ('student__first_name', 'student__last_name', 'exam__name')
    list_filter = ('is_absent', 'exam__exam_type')
    ordering = ('-created_at',)
