from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Faculty(models.Model):
    """Faculty/Teacher entity — stores department staff details."""
    DESIGNATION_CHOICES = [
        ('Professor', 'Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Assistant Professor', 'Assistant Professor'),
        ('Lecturer', 'Lecturer'),
        ('Instructor', 'Instructor'),
    ]
    name = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES, default='Lecturer')
    qualification = models.CharField(max_length=200, blank=True)
    hire_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Faculty'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.designation})"


class Course(models.Model):
    """Academic program/course (e.g., BSc CSIT, BCA, MBA)."""
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    duration_years = models.PositiveIntegerField(default=4)
    total_semesters = models.PositiveIntegerField(default=8)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.code})"

    def student_count(self):
        return self.students.filter(is_active=True).count()


class Subject(models.Model):
    """A subject/paper belonging to a course and taught by faculty."""
    SUBJECT_TYPE_CHOICES = [
        ('Theory', 'Theory'),
        ('Practical', 'Practical'),
        ('Theory & Practical', 'Theory & Practical'),
    ]
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subjects')
    faculty = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    semester = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    credit_hours = models.PositiveIntegerField(default=3)
    subject_type = models.CharField(max_length=30, choices=SUBJECT_TYPE_CHOICES, default='Theory')
    full_marks = models.PositiveIntegerField(default=100)
    pass_marks = models.PositiveIntegerField(default=40)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['course', 'semester', 'name']

    def __str__(self):
        return f"{self.name} ({self.code}) - Sem {self.semester}"


class Student(models.Model):
    """Student entity — personal and academic information."""
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Graduated', 'Graduated'),
        ('Suspended', 'Suspended'),
    ]
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    date_of_birth = models.DateField()
    address = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, related_name='students')
    current_semester = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(12)])
    enrollment_year = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    guardian_name = models.CharField(max_length=200, blank=True)
    guardian_phone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['student_id']

    def __str__(self):
        return f"{self.student_id} - {self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Enrollment(models.Model):
    """
    Junction entity linking a Student to a Subject.
    1NF: atomic fields; 2NF: no partial dependencies on PK;
    3NF: no transitive dependencies.
    """
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Dropped', 'Dropped'),
        ('Completed', 'Completed'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'subject')
        ordering = ['-enrolled_date']

    def __str__(self):
        return f"{self.student.full_name} → {self.subject.name}"


class Exam(models.Model):
    """Examination entity — an exam event for a subject."""
    EXAM_TYPE_CHOICES = [
        ('Mid-Term', 'Mid-Term'),
        ('Final', 'Final'),
        ('Practical', 'Practical'),
        ('Assignment', 'Assignment'),
        ('Quiz', 'Quiz'),
        ('Internal', 'Internal'),
    ]
    name = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    exam_type = models.CharField(max_length=30, choices=EXAM_TYPE_CHOICES, default='Final')
    exam_date = models.DateField()
    max_marks = models.PositiveIntegerField(default=100)
    pass_marks = models.PositiveIntegerField(default=40)
    academic_year = models.CharField(max_length=20, help_text='e.g. 2024-25')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-exam_date']

    def __str__(self):
        return f"{self.name} — {self.subject.code} ({self.exam_type})"


class Result(models.Model):
    """
    Result entity — marks a student scored in an exam.
    Grade is computed (not stored) to satisfy 3NF.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    marks_obtained = models.DecimalField(
        max_digits=6, decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    remarks = models.TextField(blank=True)
    is_absent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'exam')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student.full_name} | {self.exam.name}: {self.marks_obtained}"

    @property
    def percentage(self):
        if self.exam.max_marks == 0:
            return 0
        return round((float(self.marks_obtained) / self.exam.max_marks) * 100, 2)

    @property
    def grade(self):
        """Computed grade — satisfies 3NF (not stored in DB)."""
        if self.is_absent:
            return 'AB'
        p = self.percentage
        if p >= 90:
            return 'A+'
        elif p >= 80:
            return 'A'
        elif p >= 70:
            return 'B+'
        elif p >= 60:
            return 'B'
        elif p >= 50:
            return 'C+'
        elif p >= 40:
            return 'C'
        else:
            return 'F'

    @property
    def grade_point(self):
        grade_map = {
            'A+': 4.0, 'A': 3.7, 'B+': 3.3, 'B': 3.0,
            'C+': 2.7, 'C': 2.3, 'F': 0.0, 'AB': 0.0
        }
        return grade_map.get(self.grade, 0.0)

    @property
    def is_pass(self):
        return not self.is_absent and float(self.marks_obtained) >= self.exam.pass_marks
