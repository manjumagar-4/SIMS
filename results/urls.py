from django.urls import path
from . import views
urlpatterns = [
    path('', views.result_list, name='result-list'),
    path('<int:pk>/', views.result_detail, name='result-detail'),
    path('add/', views.result_create, name='result-create'),
    path('<int:pk>/edit/', views.result_update, name='result-update'),
    path('<int:pk>/delete/', views.result_delete, name='result-delete'),
    path('report/', views.result_report, name='result-report'),
    path('report/student/<int:student_id>/', views.student_report, name='student-report'),
]
