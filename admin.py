from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import Semester, Course, Instructor, Student, Assignment

## TODO: add pragmatic admin options for errthing


class SemesterAdmin(admin.ModelAdmin):
    pass


class CourseAdmin(admin.ModelAdmin):
    pass


class InstructorAdmin(admin.ModelAdmin):
    pass


class StudentAdmin(admin.ModelAdmin):
    pass


class AssignmentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Semester)
admin.site.register(Course)
admin.site.register(Instructor)
admin.site.register(Student)
admin.site.register(Assignment)

#
#
# class InstructorInline(admin.StackedInline):
#     model = Instructor
#     can_delete = False
#     verbose_name_plural = 'instructors'
#
#
# class UserAdmin():
#     inlines = (InstructorInline, )


#admin.site.unregister(User)
#admin.site.register(User, UserAdmin)
