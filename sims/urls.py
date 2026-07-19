from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('students/', include('students.urls')),
    path('courses/', include('courses.urls')),
    path('subjects/', include('subjects.urls')),
    path('faculty/', include('faculty.urls')),
    path('enrollments/', include('enrollments.urls')),
    path('exams/', include('exams.urls')),
    path('results/', include('results.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
