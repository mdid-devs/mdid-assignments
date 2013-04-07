from django.contrib.auth.models import User, Group
from rooibos.presentation.models import Presentation
from rooibos.access.models import AccessControl
from django.contrib.contenttypes.models import ContentType


def _proof_of_concept(do_it, default=False):
    """
    This is a function containing the code for creating an individual presenation for
    each member of a specified group, and giving Read perms on that presentation to the group
    Note: this is really just copied & pasted from the command line
    :param do_it: whether or not this function actually executes. Don't actually pass True, unless you're too curious
    :param default: False
    :return: None
    """
    # get a variable for member users of group 'environment_sp13_sec12'
    cl = User.objects.filter(groups__name='environment_sp13_sec12')

    for u in cl:
        pres = Presentation.objects.create(title=u'Environment photo essay', owner=u)
        acl = AccessControl.objects.create(content_type=ContentType.objects.get(id=39), object_id=pres.id,
                                           usergroup=Group.objects.get(name='environment_sp13_sec12'), read=True)