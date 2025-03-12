from django import forms
from .models import Course, Lesson, Student

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'duration', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'thumbnail': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
        
class CourseEnrollmentForm(forms.Form):
    student_name = forms.CharField(label="Full Name", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    student_email = forms.EmailField(label="Student Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    course = forms.ModelChoiceField(queryset=Course.objects.all(), label="Select Course", widget=forms.Select(attrs={'class': 'form-control'}))