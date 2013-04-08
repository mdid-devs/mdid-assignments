from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from models import Course, Instructor, Student, Assignment

## TODO: add similar manager code for Courses, Students, Assignment Listings & Assignment Objects


class InstructorInline(admin.StackedInline):
    model = Instructor
    can_delete = False
    verbose_name_plural = 'instructors'


class UserAdmin():
    inlines = (InstructorInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
