from django.urls import path
from . import views

urlpatterns = [
    # path('', views.base, name='base'),
    path('', views.home, name='home'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/edit/<int:course_id>/', views.edit_course, name='edit_course'),  # Add this URL
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    
    # Lesson URLs
    path('courses/<int:course_id>/lessons/add/', views.add_lesson, name='add_lesson'),
    path('lessons/edit/<int:lesson_id>/', views.edit_lesson, name='edit_lesson'),
    path('lessons/delete/<int:lesson_id>/', views.delete_lesson, name='delete_lesson'),
]
