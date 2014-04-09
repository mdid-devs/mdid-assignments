from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

from django.forms.extras.widgets import SelectDateWidget

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

    def __unicode__(self):
        return self.name


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


class Student(models.Model):
    """
    defines a Student
    """
    user = models.OneToOneField(User)
    courses = models.ManyToManyField(Course, blank=True)


class Semester(models.Model):
    """
    defines a Semester, i.e. a name for a period of time
    """
    period = models.CharField(max_length=50,
                              choices=SEMESTER_CHOICES,
                              blank=True)
    year = models.IntegerField(max_length=4)
    start = models.DateField(auto_now=False,
                             auto_now_add=False,
                             blank=True)
    end = models.DateField(auto_now=False,
                           auto_now_add=False,
                           blank=True)

    def __unicode__(self):
        return ' '.join((Semester.base.value_to_string(self), Semester.year.value_to_string(self)))


class Assignment(models.Model):
    """
    The assignment object as created by the instructor
    """
    name = models.CharField(max_length=100)
    due_date = models.DateTimeField(SelectDateWidget)  # TODO: why won't it accept widget=SelectDateWidget() ?
    courses = models.ManyToManyField(Course)

    def __unicode__(self):
        return self.name


class PresentationAssignment(models.Model):
    """
    associates a presentation object to an assignment, so an instructor can review
    the presentation can be named anything, the link is preserved by the listing attribute
    """
    name = models.CharField(max_length=100)
    listing = models.ForeignKey(Assignment_Listing)
    course = models.ForeignKey(Course)
    submission_date = models.DateField(default=None)
    assignee = models.ManyToManyField(User)

    def __unicode__(self):
        return self.name
