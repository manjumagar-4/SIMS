from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_list, name='student-list'),
    path('<int:pk>/', views.student_detail, name='student-detail'),
    path('add/', views.student_create, name='student-create'),
    path('<int:pk>/edit/', views.student_update, name='student-update'),
    path('<int:pk>/delete/', views.student_delete, name='student-delete'),
]
