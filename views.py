from django.http import Http404
from django.template import TemplateDoesNotExist
from django.views.generic.simple import direct_to_template


def listings(request):
    try:
        return direct_to_template(request, template="listings.html")
    except TemplateDoesNotExist:
        raise Http404()