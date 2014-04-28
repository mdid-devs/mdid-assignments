from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.contrib.contenttypes import generic
from django.db import IntegrityError
from rooibos.presentation.models import Presentation as rooibosPresentation
import logging
# semester names are defined in apps.mdid-settings.settings.py
from settings import SEMESTER_CHOICES


class LTIUser(models.Model):
    """
    The user profile assumes an LTI integration, but all of the LTI specific data
    is optional so that it's not necessary to have an integration to use the assignment feature
    """
    user = models.ForeignKey(User, related_name='lti')
    lti_user_id = models.CharField(max_length=255, blank=True, default=None, null=True)
    lti_lis_person_name_given = models.CharField(max_length=255, default=None, blank=True, null=True)
    lti_lis_person_name_family = models.CharField(max_length=255, default=None, blank=True, null=True)
    lti_lis_person_name_full = models.CharField(max_length=255, default=None, blank=True, null=True)
    lti_lis_person_contact_email_primary = models.EmailField(default=None, blank=True, null=True)

    def __unicode__(self):
        return self.user.username


class LTIObject(models.Model):
    """
    Maps LTI data to specific objects to avoid redundant database fields in each model
    Every field may not apply to each object.
    """
    object = models.ForeignKey(ContentType,
                               limit_choices_to={'model__in': ('course',
                                                               'assignment',
                                                               'courselink', )}, )
    lti_custom_handle = models.CharField(max_length=32, help_text='A custom handle passed by the LMS - '
                                                                  'it is necessary to configure your LMS to '
                                                                  'pass this value. Please see readme.md')
    lti_context_label = models.CharField(max_length=255, help_text='LMS course id',
                                         blank=True, default=None, null=True)
    lti_context_id = models.CharField(max_length=255, help_text='Uniquely identifies the context containing the link',
                                      blank=True, default=None, null=True)
    lti_context_title = models.CharField(max_length=255, help_text='lms course title',
                                         blank=True, default=None, null=True)
    lti_resource_link_title = models.CharField(max_length=255)
    lti_resource_link_id = models.CharField(max_length=255, null=True, blank=True, default=None)
    lti_launch_presentation_return_url = models.URLField(null=True, blank=True, default=None)
    lti_lis_outcome_service_url = models.URLField(null=True, blank=True, default=None)
    created_by = models.ForeignKey('LTIUser')
    created_with = models.CharField(max_length=255, null=True, blank=True, default=None)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


class Course(models.Model):
    """
    The basic intuitive organizing unit - note: users are organized via CourseRoster
    """
    # TODO: Does it make sense to create groups as well? Or is that just redundant clutter?
    # TODO: add function to create course groups automatically?

    title = models.CharField(max_length=255,
                             help_text='The title of the course',
                             blank=False,
                             default=None,
                             null=False)
    name = models.SlugField(max_length=255, unique=True)
    semester = models.ForeignKey('Semester', default=None, blank=True, null=True)
    members = models.ManyToManyField('LTIUser', through='CourseRoster')
    lti_object = models.ForeignKey('LTIObject')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        def slug_exists(slug):
            return Course.objects.get(name=slug)

        title_slug = slugify(self.title + self.semester.__unicode__())

        if not slug_exists(title_slug):
            self.name = title_slug
        else:
            self.name = '%s-%i' % (
                slugify(self.title + self.semester.__unicode__()), self.id
            )

        super(Course, self).save(*args, **kwargs)

    # TODO: Course.add_student_by_username?
    def add_student_by_username(self, username):
        pass

    def add_instructor_by_username(self, username):
        pass


class CourseRoster(models.Model):
    person = models.ForeignKey('LTIUser')
    for_course = models.ForeignKey('Course')
    is_instructor = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Course roster for %s' % self.for_course.name

    def is_student(self):
        return not self.is_instructor


class Semester(models.Model):
    """
    defines a Semester, i.e. a name for an arbitrary period of time - these should be unique so once one is defined it
    should be reused by everybody. This may need to be an admin-defined system

    Currently if no semester is set semester.__unicode__ will return 'Continuous'
    """
    name = models.SlugField(max_length=56, unique=True, editable=False)
    period = models.CharField(max_length=50,
                              choices=SEMESTER_CHOICES,
                              blank=True,
                              default=None,
                              null=True)
    year = models.IntegerField(max_length=4)
    start = models.DateField(auto_now=False,
                             auto_now_add=False,
                             blank=True,
                             default=None,
                             null=True)
    end = models.DateField(auto_now=False,
                           auto_now_add=False,
                           blank=True,
                           default=None,
                           null=True)

    def __unicode__(self):
        reply = 'Continuous'
        if self.period and self.year:
            reply = ' '.join((self.period, str(self.year)))

        return reply

    def save(self, *args, **kwargs):

        if not self.name:
            title_slug = slugify(self.name + self.period)
            self.name = title_slug

            while True:
                try:
                    super(Semester, self).save(*args, **kwargs)
                except Exception as e:
                    logging.debug(e)
                    break

                    # TODO: Override save method so semesters are not duplicated

                    # TODO: Should semesters be automatically created from settings.SEMESTER_CHOICES if they don't exist for a date?
                    # i.e. on Jan 2 2015 auto create 'Fall 2015', 'Spring 2015' etc. and let an admin edit the dates if necessary?


                ## assignments
                # TODO: write a function that gets all Assignments that point to a specific course
                # TODO: confirm an efficient model for supporting multiple assignment types DRY style
                # i.e. one Assignment obj with related classes not separate Assignment classes,


class Assignment(models.Model):
    """
    The assignment object as created by a course instructor. An assignment is owned by a course,
    not the instructor LTIUser. There are multiple types of assignment (presentation & e-portfolio)
    """
    help_text = "Assignments "
    name = models.CharField(max_length=100)
    #assignment_type = models.ForeignKey(ContentType,
    #                                    limit_choices_to={'model__in': ('PresentationAssignment', )}, )
    available_date = models.DateTimeField(default=None, blank=True)
    due_date = models.DateTimeField(default=None, blank=True)
    course = models.ForeignKey(Course, default=None, blank=True)
    submissions = models.ManyToManyField('AssignmentSubmission')
    lti_object = models.ForeignKey('LTIObject')

    def __unicode__(self):
        return self.name


class AssignmentSubmission(models.Model):
    complete = models.BooleanField(default=False)
    submission_date = models.DateTimeField(auto_now=True)
    #submission_content = models.ForeignKey('Assignment', to_field='assignment_type')
    assignment_type = models.ForeignKey(ContentType,
                                        limit_choices_to={'model__in': ('PresentationAssignment', )}, )
    assignee = models.ManyToManyField('LTIUser', related_name='assignments')


class PresentationAssignment(rooibosPresentation):
    """
    Extends the standard MDID presentation object to an assignment, so an instructor can
    the presentation can be named anything, the link is preserved by the listing attribute
    """
    assignment = models.ForeignKey('Assignment')
    minimum_items = models.IntegerField(blank=True, default=None,
                                        help_text='The minimum required number of items '
                                                  '(leave blank for no requirement)')
    maximum_items = models.IntegerField(blank=True, default=None,
                                        help_text='The maximum allowed number of items '
                                                  '(leave blank for no limit)')

    def __unicode__(self):
        return self.name


##  content links


class CourseLink(models.Model):
    title = models.CharField(max_length=255, blank=True, default=None, null=True)
    lti_object = models.ForeignKey('LTIObject')


class CourseLinkRelation(models.Model):
    course_link = models.ForeignKey(CourseLink)
    link_type = models.ForeignKey(ContentType, limit_choices_to={'model__in': ('presentation', 'record')}, )
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')




    # TODO : design a class for user-owned-work records (i.e. extends Record with additional features for assessment