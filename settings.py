import os
import rooibos.settings



# TODO: If set to True user info in MDID (first & last name, email) will be overwritten
ALLOW_LMS_USER_INFO_SYNC = False

# TODO: is something like dynamically registering the app name based on the enclosing directory name possible?
#COURSE_APP = os.path.dirname(__file__).__module__

INSTALLED_APPS = (
    #COURSE_APP,
    'apps.mdid-assignments',
)

LTI_DEBUG = True
LTI_CONSUMER_KEY = 'lti'
LTI_SECRET = '123'
LTI_FIRST_NAME = 'lis_person_name_given'
LTI_LAST_NAME = 'lis_person_name_family'
LTI_EMAIL = 'lis_person_contact_email_primary'
LTI_ROLES = 'roles'
LTI_USER_ID_SCHEME = 'local'

LTI_INSTRUCTOR_ROLES = ['Instructor', ]
LTI_C_USERNAME = 'custom_username'

LTI_C_HANDLE = 'custom_handle'
LTI_HANDLE_COURSE = 'course'
LTI_HANDLE_CONTENT = 'content_link'
LTI_HANDLE_ASSIGNMENT = 'assignment'


#### USER_ID_SCHEME
# this setting determines how Users created by lti have User.username generated
# see http://developers.imsglobal.org/userid.html for guidance on how to choose a scheme
# valid choices are
# local: username from LMS (for institutions where a username is the unique id for user accounts)
#     May require sending a custom field, e.g. in Blackboard adding 'username=@X@user.id@X@'
# global: user_id parameter;
# consumer: combine the consumer key with the user_id parameter;
# context: combine the consumer key with the context_id and user_id parameters;
# resource link: combine the consumer key with the resource_link_id and user_id parameters.


TEMPLATE_DIRS = (
    os.path.normpath(os.path.join(os.path.dirname(__file__), 'templates')),
)

STATICFILES_DIRS = (
     os.path.normpath(os.path.join(os.path.dirname(__file__), 'static')),
)

# Semester choices sets available nomenclature for semesters.
SEMESTER_CHOICES = (
    (u'Fa', u'Fall'), (u'Sp', u'Spring'), (u'S1', u'Summer 1'), (u'S2', u'Summer 2'), (u'O', u'Other'),
)
