# if needed

ROOT_URLCONF = 'rooibos.apps.mdid-assignments.urls'

INSTALLED_APPS = (
    'apps.mdid-assignments',
)

# Semester choices sets available nomenclature for semesters.
SEMESTER_CHOICES = (
    ('Fa', 'Fall'), ('Sp', 'Spring'), ('S1', 'Summer 1'), ('S2', 'Summer 2'), ('O', 'Other'),
)
