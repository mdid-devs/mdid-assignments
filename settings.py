import os
import rooibos.settings

from rooibos.settings import TEMPLATE_DIRS

# if needed

#ROOT_URLCONF = 'rooibos.apps.mdid-assignments.urls'

INSTALLED_APPS = (
    'apps.mdid-assignments',
)

TEMPLATE_DIRS = (
    os.path.normpath(os.path.join(os.path.dirname(__file__), 'templates')),
)

# Semester choices sets available nomenclature for semesters.
SEMESTER_CHOICES = (
    (u'Fa', u'Fall'), (u'Sp', u'Spring'), (u'S1', u'Summer 1'), (u'S2', u'Summer 2'), (u'O', u'Other'),
)
