
from .models import Course
from django.shortcuts import render, get_object_or_404
from .models import Course,Lesson, Student

from django.shortcuts import render, redirect
from .forms import CourseForm, LessonForm, CourseEnrollmentForm

from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render, get_object_or_404, redirect



def base(request):
    return render(request, 'base.html')  # Correct
def home(request):
    return render(request, 'home.html')  # Correct

def description(request):
    return render(request, 'description.html')  # You can create a template 'description.html' for this page

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})


# courses/views.py
from django.shortcuts import render, get_object_or_404
from .models import Course

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)  # Get the course by its ID
    lessons = course.lessons.all()  # Fetch all lessons for this course
    return render(request, 'courses/course_detail.html', {'course': course, 'lessons': lessons})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)  # Handle form data and file upload
        if form.is_valid():
            form.save()  # Save the new course to the database
            return redirect('course_list')  # Redirect to the course list after adding the course
    else:
        form = CourseForm()
    
    return render(request, 'courses/add_course.html', {'form': form})

def delete_course_confirm(request, id):
    # Get the course object for confirmation
    course = get_object_or_404(Course, id=id)

    if request.method == 'POST':  # If the user confirms deletion
        course.delete()  # Delete the course
        return redirect('course_list')  # Redirect to the course list page

    return render(request, 'courses/course_confirm_delete.html', {'course': course})
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')  # Redirect back to the course list after saving the course
    else:
        form = CourseForm(instance=course)

    return render(request, 'courses/edit_course.html', {'form': form, 'course': course})




def add_lesson(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.course = course
            lesson.save()
            return redirect('course_detail', course_id=course.id)
    else:
        form = LessonForm()
    
    return render(request, 'courses/add_lesson.html', {'form': form, 'course': course})

def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            return redirect('course_detail', course_id=lesson.course.id)
    else:
        form = LessonForm(instance=lesson)

    return render(request, 'courses/edit_lesson.html', {'form': form, 'lesson': lesson})

def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course_id = lesson.course.id
    lesson.delete()
    return redirect('course_detail', course_id=course_id)

def delete_lesson_confirm(request, lesson_id):
    # Get the lesson object to be deleted
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        # If confirmed, delete the lesson and redirect
        lesson.delete()
        return redirect('course_detail', course_id=lesson.course.id)  # Adjust this URL as needed

    # If it's a GET request, show the confirmation page
    return render(request, 'courses/lesson_delete_confirmation.html', {'lesson': lesson})

def enroll_student(request):
    if request.method == 'POST':
        form = CourseEnrollmentForm(request.POST)
        if form.is_valid():
            student_name = form.cleaned_data['student_name']
            student_email = form.cleaned_data['student_email']
            course = form.cleaned_data['course']

            # Get or create the student
            student, created = Student.objects.get_or_create(email=student_email)
            student.name = student_name  # Save the name if not already set
            student.save()

            # Enroll the student in the selected course
            student.enrolled_course.add(course)

            # Redirect to the success page
            return render(request, 'courses/enrollment_success.html', {'student': student, 'course': course})
    else:
        form = CourseEnrollmentForm()

    return render(request, 'courses/enroll_student.html', {'form': form})