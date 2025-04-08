from django.urls import path
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)
from .views import register, user_login, user_logout, profile, profile_update
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('', views.base, name='base'),
    path("", views.home, name="home"),
    path("courses/", views.course_list, name="course_list"),
    path("courses/<int:course_id>/", views.course_detail, name="course_detail"),
    path("courses/edit/<int:course_id>/", views.edit_course, name="edit_course"),  
    path("courses/add/", views.add_course, name="add_course"),
    # path('courses/delete/<int:course_id>/', views.delete_course, name='delete_course'),
    path("course/<int:id>/delete/",views.delete_course_confirm,name="delete_course_confirm",),
    # Lesson URLs
    path("courses/<int:course_id>/lessons/add/", views.add_lesson, name="add_lesson"),
    path("lessons/edit/<int:lesson_id>/", views.edit_lesson, name="edit_lesson"),
    path("delete_lesson_confirm/<int:lesson_id>/",views.delete_lesson_confirm,name="delete_lesson_confirm",),
    # enroll urls
    path("enroll/", views.enroll_student, name="enroll_student"),
    path("course/<int:course_id>/enrolled/",views.view_enrolled_students,name="view_enrolled_students",),
    # authentication
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("profile/", profile, name="profile"),
    path("profile/update", profile_update, name="profile_update"),
    path("password_change/",auth_views.PasswordChangeView.as_view(template_name="courses/password_change.html"),name="password_change",),
    path("password_change/done/",auth_views.PasswordChangeDoneView.as_view(template_name="courses/password_change_done.html"),name="password_change_done",),
    # password reset
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password_reset_complete/", CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
