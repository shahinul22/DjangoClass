from django.contrib import admin
from django.utils.html import format_html  # Import format_html for rendering HTML
from .models import Course, Lesson, Student

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'thumbnail_preview')

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:5px;"/>', obj.thumbnail.url)
        return "No Image"

    thumbnail_preview.short_description = "Thumbnail Preview"

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson)
admin.site.register(Student)
