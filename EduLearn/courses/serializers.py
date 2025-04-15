from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Course, Lesson, Student

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'course', 'title', 'content', 'video_url', 'completion_status']

class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'duration', 'thumbnail', 'created_at', 'lessons']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    enrolled_courses = CourseSerializer(many=True, read_only=True)
    completed_lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'user', 'name', 'email', 'enrolled_courses', 'completed_lessons']


