from django.contrib.auth.models import User, Group
from rooibos.presentation.models import Presentation
from rooibos.access.models import AccessControl
from django.contrib.contenttypes.models import ContentType


def _original_presentation_creation_proof_of_concept(do_it, default=False):
    """
    This is a function containing the code for creating an individual presenation for
    each member of a specified group, and giving Read perms on that presentation to the group
    Note: this is really just copied & pasted from the command line
    Note : If you've read this far, I salute you.
    :param do_it: whether or not this function actually executes. Don't actually pass True, unless you're too curious
    :param default: False
    :return: None
    """
    # get a variable for member users of group 'group_containing_course_members'
    cl = User.objects.filter(groups__name='group_containing_course_members')

    for u in cl:
        pres = Presentation.objects.create(title=u'Assigned Presentation', owner=u)
        acl = AccessControl.objects.create(content_type=ContentType.objects.get(id=39), object_id=pres.id,
                                           usergroup=Group.objects.get(name='group_containing_course_members'), read=True)