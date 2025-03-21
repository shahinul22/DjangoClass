
from .models import Course
from django.shortcuts import render, get_object_or_404
from .models import Course,Lesson, Student

from django.shortcuts import render, redirect
from .forms import CourseForm, LessonForm, CourseEnrollmentForm

from django.shortcuts import render, redirect, get_object_or_404

from django.shortcuts import render, get_object_or_404, redirect



# for authentication 
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserUpdateForm

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
            messages.success(request, "Course added successfully!")
            return redirect('course_list')  # Redirect to the course list after adding the course
        else:
            messages.error(request, "Error adding course. Please try again.")
    else:
        messages.error(request, "Error adding course. Please try again.")
        form = CourseForm()
    
    return render(request, 'courses/add_course.html', {'form': form})

def delete_course_confirm(request, id):
    # Get the course object for confirmation
    course = get_object_or_404(Course, id=id)

    if request.method == 'POST':  # If the user confirms deletion
        course.delete()  # Delete the course
        messages.success(request, "Course deleted successfully!")
        return redirect('course_list')  # Redirect to the course list page

    return render(request, 'courses/course_confirm_delete.html', {'course': course})
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated course details")
            return redirect('course_list')  # Redirect back to the course list after saving the course
        else:
            messages.error(request, "Error adding course. Please try again.")
    else:
        # messages.error(request, "Error adding course. Please try again.")
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
            messages.success(request, "Lesson added successfully!")
            return redirect('course_detail', course_id=course.id)
        else:
            messages.error(request, "Error adding course. Please try again.")
    else:
        # messages.error(request, "Error adding course. Please try again.")
        form = LessonForm()
    
    return render(request, 'courses/add_lesson.html', {'form': form, 'course': course})

def edit_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated lesson details")
            return redirect('course_detail', course_id=lesson.course.id)
        else:
            messages.error(request, "Error adding course. Please try again.")
    else:
        # messages.error(request, "Error adding course. Please try again.")
        form = LessonForm(instance=lesson)

    return render(request, 'courses/edit_lesson.html', {'form': form, 'lesson': lesson})

def delete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    course_id = lesson.course.id
    lesson.delete()
    # messages.success(request, "Lesson deleted successfully!")
    return redirect('course_detail', course_id=course_id)

def delete_lesson_confirm(request, lesson_id):
    # Get the lesson object to be deleted
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == 'POST':
        # If confirmed, delete the lesson and redirect
        lesson.delete()
        messages.success(request, "Lesson deleted successfully!")
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

            # Check if the student is already enrolled in the selected course
            if student.enrolled_course.filter(id=course.id).exists():
                # If already enrolled, display a message
                messages.warning(request, f"{student.name}, you are already enrolled in {course.title}.")
                return render(request, 'courses/enrollment_success.html', {
                    'student': student,
                    'course': course,
                    'already_enrolled': True  # Flag to indicate the student is already enrolled
                })

            # Enroll the student in the selected course
            messages.success(request, f"Congratulations {student.name}! You have been enrolled in {course.title}.")
            student.enrolled_course.add(course)

            # Redirect to the success page
            return render(request, 'courses/enrollment_success.html', {
                'student': student,
                'course': course,
                'already_enrolled': False  # Student is not already enrolled
            })
    else:
        form = CourseEnrollmentForm()

    return render(request, 'courses/enroll_student.html', {'form': form})




def view_enrolled_students(request, course_id):
    # Get the course object by its ID
    course = get_object_or_404(Course, id=course_id)
    
    # Get the list of students enrolled in this course (ManyToMany relation)
    enrolled_students = course.students.all()  # Accessing students through the related_name 'students'

    return render(request, 'courses/view_enrolled_students.html', {
        'course': course,
        'enrolled_students': enrolled_students
    })
    
    
# authentication

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect("login")  # Redirect to login page after successful registration
        else:
            messages.error(request, "Registration failed. Please check the form for errors.")
    else:
        form = UserCreationForm()

    return render(request, "courses/register.html", {"form": form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('/')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'courses/login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('/')


from django.contrib.auth.decorators import login_required

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})



@login_required
def profile(request):
    user = request.user
    return render(request, "courses/profile.html", {"user": user})


@login_required
def profile_update(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, 'courses/profile_update.html', {'form': form})


