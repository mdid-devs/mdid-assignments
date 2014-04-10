from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django import forms
from django.forms.extras.widgets import SelectDateWidget
from rooibos.util import unique_slug

# semester names are defined in apps.mdid-settings.settings.py
from settings import SEMESTER_CHOICES


class Course(models.Model):
    """
    a model for a standard lms course - basically just an indexing thing at this point
    """
    name = models.SlugField(max_length=50, unique=True)
    course_groups = models.ForeignKey(Group)
    # instructors uses a 'string' instead of a name because Instructor is defined elsewhere. What?
    instructors = models.ManyToManyField('Instructor')
    students = models.ManyToManyField('Student')

    def __unicode__(self):
        return self.name

    def add_student_by_username(self, username):
        pass


class Instructor(models.Model):
    """
    defines an instructor user
    """
    user = models.OneToOneField(User)
    courses = models.ManyToManyField(Course, blank=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        ordering = ('user',)

    def add_instructor_by_username(self, username):
        pass


class Student(models.Model):
    """
    defines a Student
    """
    user = models.OneToOneField(User)
    courses = models.ManyToManyField(Course, blank=True)
    assignments = models.ManyToManyField('Assignment', blank=True)

    def __unicode__(self):
        return self.user.username


class Semester(models.Model):
    """
    defines a Semester, i.e. a name for an arbitrary period of time
    """
    name = models.SlugField(max_length=50, unique=True, editable=False)
    period = models.CharField(max_length=50,
                              choices=SEMESTER_CHOICES,
                              blank=True)
    year = models.IntegerField(max_length=4)
    start = models.DateField(auto_now=False,
                             auto_now_add=False,
                             blank=True,
    )
    end = models.DateField(auto_now=False,
                           auto_now_add=False,
                           blank=True,
    )

    def __unicode__(self):
        return ' '.join((Semester.base.value_to_string(self), Semester.year.value_to_string(self)))

    def save(self, force_update_name=False, **kwargs):
        unique_slug(self, slug_literal=self.__unicode__(),
                    slug_field='name', check_current_slug=kwargs.get('force_insert') or force_update_name)
        super(Semester, self).save(kwargs)


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ('start', 'end', 'year')
        widgets = {
            'start': SelectDateWidget(),
            'end': SelectDateWidget(),
        }


class Assignment(models.Model):
    """
    The assignment object as created by the instructor
    """
    help_text = "Assignments "
    name = models.CharField(max_length=100)
    due_date = models.DateTimeField(default=None, blank=True)
    course = models.ManyToManyField(Course)
    submissions = models.ManyToManyField('PresentationAssignment', blank=True)

    def __unicode__(self):
        return self.name


class PresentationAssignment(models.Model):
    """
    associates a presentation object to an assignment, so an instructor can review
    the presentation can be named anything, the link is preserved by the listing attribute
    """
    title = models.CharField(max_length=100)
    name = models.SlugField(max_length=100, unique=True, blank=True)
    listing = models.ForeignKey(Assignment)
    course = models.ForeignKey(Course)
    submission_date = models.DateTimeField(auto_now=True)
    assignee = models.ManyToManyField(Student)

    def __unicode__(self):
        return self.name
