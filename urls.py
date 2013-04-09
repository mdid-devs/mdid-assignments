from django.conf.urls.defaults import *
from models import *

course_list = {
    'queryset': Course.objects.all()
}

urlpatterns = patterns('',
    # Example:
    (r'^dashboard/', include('listings')),

)
