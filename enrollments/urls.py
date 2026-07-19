from django.urls import path
from . import views
urlpatterns = [
    path('', views.enrollment_list, name='enrollment-list'),
    path('add/', views.enrollment_create, name='enrollment-create'),
    path('<int:pk>/edit/', views.enrollment_update, name='enrollment-update'),
    path('<int:pk>/delete/', views.enrollment_delete, name='enrollment-delete'),
]
