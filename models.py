from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

from django.forms.extras.widgets import SelectDateWidget


class Course(models.Model):
    """
    a model for a standard lms course - basically just an indexing thing at this point
    """
    name = models.SlugField(max_length=50, unique=True)
    course_groups = models.ForeignKey(Group)
    instructors = models.ManyToManyField(Instructor)

    def __unicode__(self):
        return self.name


class Instructor(models.Model):
    """
    defines an instructor user
    """
    user = models.OneToOneField(User)
    courses = models.ManyToManyField(Course)

    def __unicode__(self):
        return self.account.username

    class Meta:
        ordering = ('account_name',)


class Student(models.Model):
    """
    defines a Student
    """
    user = models.OneToOneField(User)


class Assignment_Listing(models.Model):
    """
    The assignment object as created by the instructor
    """
    name = models.CharField(max_length=100)
    due_date = models.DateTimeField(widget=SelectDateWidget())
    courses = models.ManyToManyField(Course)

    def __unicode__(self):
        return self.name


class Assignment(models.Model):
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
