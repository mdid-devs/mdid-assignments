from django.conf.urls.defaults import *
from models import Course
from rooibos.urls import urls

urls.append(url(r'^courses/', include('rooibos.apps.mdid-assignments.urls')))

#course_list = {
#    'queryset': Course.objects.all()
#}

urlpatterns = patterns('rooibos.apps.mdid-assignments.views',
    # /courses/
    (r'^lti/$', 'launch_lti'),
    (r'^$', 'courses_main'),
    (r'^(?P<course_name>)/$', 'this_is_lame_view'),  # temp 'unimplemented' view



)
