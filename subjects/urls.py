from django.urls import path
from . import views
urlpatterns = [
    path('', views.subject_list, name='subject-list'),
    path('add/', views.subject_create, name='subject-create'),
    path('<int:pk>/edit/', views.subject_update, name='subject-update'),
    path('<int:pk>/delete/', views.subject_delete, name='subject-delete'),
]
