from django.urls import path
from . import views
urlpatterns = [
    path('', views.faculty_list, name='faculty-list'),
    path('<int:pk>/', views.faculty_detail, name='faculty-detail'),
    path('add/', views.faculty_create, name='faculty-create'),
    path('<int:pk>/edit/', views.faculty_update, name='faculty-update'),
    path('<int:pk>/delete/', views.faculty_delete, name='faculty-delete'),
]
