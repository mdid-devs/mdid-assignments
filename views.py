from django.http import Http404
from django.template import TemplateDoesNotExist
from django.views.generic.simple import direct_to_template
from django.contrib.formtools.wizard import FormWizard
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from ims_lti_py.tool_provider import DjangoToolProvider
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.conf import settings
from utils import *
from models import LTIUser, LTIObject, Course, CourseRoster
import re
import logging




def courses_main(request):
    """
    A dashboard for any user logged into mdid3 that allows access to any courses the user is enrolled
    in or teaching. It is assumed that it will be common enough for individual users to be able to straddle
    both roles that both courses being taught and being taken should be shown.
    """
    lti_user = LTIUser.objects.get(user=request.user)

    as_instructor = {}
    as_student = {}

    #as_student = Course.objects.filter(students__contains=lti_user)
    #
    #as_instructor = lti_user.courses_teaching.filter()
    #as_student = lti_user.courses_taking.filter()

    return direct_to_template(request, 'courses_main.html', {'out': '<h1>TODO: This view</h1>',
                                                             'as_instructor': as_instructor,
                                                             'as_student': as_student})


def course_view(request, course_name):

    course = Course.objects.get(name=course_name)

    instructors = ''
    pass

    return direct_to_template(request, 'master_root.html', {'out': '<h1>TODO: This view</h1>',
                                                            'in' : instructors})


def this_is_lame_view(request, message):
    return direct_to_template(request, 'courses_dev.html', {'out': '<h1>TODO: This</h1> '
                                                                   '<p>This part isn\'t done yet - so lame, sorry!', })


def assignment_view(request):
    pass


@csrf_exempt
def launch_lti(request):
    """ Receives a request from the lti consumer and creates/authenticates user in django """

    consumer_key = settings.LTI_CONSUMER_KEY
    secret = settings.LTI_SECRET
    tool_provider = DjangoToolProvider(consumer_key, secret, request.POST)
    request_oauth_key = get_lti_value('oauth_consumer_key', tool_provider)
    # course values
    course_id = get_lti_value('context_label', tool_provider)
    course_title = get_lti_value('context_title', tool_provider)
    course_link_id = get_lti_value('context_id', tool_provider)
    handle = get_lti_value(settings.LTI_C_HANDLE, tool_provider)
    course = None
    # user values
    r = re.split(r'[:/]', get_lti_value(settings.LTI_ROLES, tool_provider)[0])
    user_role = r[-1]
    current_user = None

    # if we're debugging let's see what's going on
    if settings.LTI_DEBUG:
        logging.debug('LTI: oauth_consumer_key: %s' % request_oauth_key)
        for item in request.POST:
            logging.debug('LTI POST: %s: %s \r' % (item, request.POST[item]))
        logging.debug("LTI:  ROLES:  %s " % tool_provider.roles)

        try:
            oauth_debug = get_lti_value('oauth_consumer_key', tool_provider)
            logging.debug('OAUTH debug: %s' % oauth_debug)
            logging.debug('OAUTH is request valid: %s' % tool_provider.is_valid_request(request))
            #logging.debug(dir(oauth_debug))

        except Exception as e:
            logging.debug('OAUTH debug: %s' % e)

    # attempt to validate request, if fails raises 403 Forbidden
    try:
        if not tool_provider.is_valid_request(request):
            raise PermissionDenied()
    except Exception as e:
        if settings.LTI_DEBUG:
            logging.debug('OAUTH debug - request not valid for oauth consumer key : %s' %
                          get_lti_value('oauth_consumer_key', tool_provider))
            logging.debug('OAUTH debug: %s' % e)
        raise PermissionDenied()

    # OKIDOKE, EVERYTHING IS OK SO NOW...

    if lti_user_auth(request, tool_provider) and handle == settings.LTI_HANDLE_CONTENT:
        # TODO: Implement content links... whoops?
        # has content already been handled?
        return HttpResponseRedirect(reverse('this_is_lame_view'))

    if lti_user_auth(request, tool_provider):
        # do course, lti_object, linked_content exist?

        try:
            course = Course.objects.get(lti_object=LTIObject.objects.get(lti_context_label=course_id))
        except ObjectDoesNotExist:

            # TODO: is it worth checking to see if the user wants to associate an existing non-associated course?
            # if not and user is instructor, create course
            for role in settings.LTI_INSTRUCTOR_ROLES:
                if settings.LTI_DEBUG:
                    logging.debug('LTI role check: POSTed role: %s vs %s' % (user_role, role))
                if role == user_role:
                    u = LTIUser.objects.get(user=request.user)

                    o = LTIObject.objects.get_or_create(lti_context_label=course_id,
                                                        lti_context_id=course_link_id,
                                                        lti_context_title=course_titlee)
                    r = CourseRoster.objects.create(person=u,
                                                    for_course=c,
                                                    is_instructor=True)
                    c = Course.objects.create(title=course_title)
                    r.save()
                    course = r
                # if course does not exist & user is not an instructor, show message
                else:
                    return direct_to_template(request, 'courses_course.html',
                                              {'message': 'This course has not been setup yet',
                                               'error': True})
      #  else:
      #      pass
            # ok, so the course already exists -

                # if course exists and user is
        #return redirect(courses_main)
    else:
        raise PermissionDenied






