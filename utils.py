import logging
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
import re
from django.template.defaultfilters import slugify
from models import LTIUser

# When a python developer has a problem, they might think...
import re
# now they have two problems!

#class LTIUserNameSchemeException(Exception):
#    pass


def get_lti_value(key, tool_provider):
    """ Searches for the given key in the tool_provider and its custom and external params.  
        If not found returns None """

    lti_value = None

    if "custom" in key:
        lti_value = tool_provider.custom_params[key]
    if "ext" in key:
        lti_value = tool_provider.ext_params[key]
    if not lti_value:
        try:
            lti_value = getattr(tool_provider, key)
        except AttributeError:
            if settings.DEBUG:
                logging.debug("Attribute: %s not found in LTI tool_provider" % key)
            pass

    return lti_value


def get_lti_user_name_by_scheme(tool_provider):
    # see mdid-assignments.settings for explanation
    lti_username = None

    if settings.LTI_USER_ID_SCHEME == 'local':
        lti_username = '%s' % get_lti_value('custom_username', tool_provider)
    elif settings.LTI_USER_ID_SCHEME == 'global':
        lti_username = '%s' % get_lti_value('user_id', tool_provider)
    elif settings.LTI_USER_ID_SCHEME == 'consumer':
        lti_username = '%s:user_%s' % (get_lti_value('oauth_consumer_key', tool_provider),
                                       get_lti_value('user_id', tool_provider))
    elif settings.LTI_USER_ID_SCHEME == 'context':
        lti_username = '%s:context_%s:userid_%s' % (get_lti_value('oauth_consumer_key', tool_provider),
                                                    get_lti_value('context_id', tool_provider),
                                                    get_lti_value('user_id', tool_provider))
    elif settings.LTI_USER_ID_SCHEME == 'resource link':
        lti_username = '%s:resource_%s:userid_%s' % (get_lti_value('oauth_consumer_key', tool_provider),
                                                     get_lti_value('context_id', tool_provider),
                                                     get_lti_value('user_id', tool_provider))
    else:
        logging.error('mdid-assignments: settings.LTI_USER_ID_SCHEME is not valid')
        raise Exception()

    return lti_username


def lti_user_auth(request, tool_provider):
    # GET OR CREATE NEW USER AND LTI_PROFILE
    # User first
    user_name = get_lti_user_name_by_scheme(tool_provider)
    # optional and lti specific
    email = get_lti_value(settings.LTI_EMAIL, tool_provider)
    roles = get_lti_value(settings.LTI_ROLES, tool_provider)
    user_id = get_lti_value('user_id', tool_provider)
    first_name = get_lti_value('lis_person_name_given', tool_provider)
    last_name = get_lti_value('lis_person_name_family', tool_provider)
    full_name = get_lti_value('lis_person_name_full', tool_provider)

    lti_data = dict(user_name=user_name, email=email,
                    roles=roles, user_id=user_id,
                    first_name=first_name, last_name=last_name,
                    full_name=full_name)
    if settings.LTI_DEBUG:
        logging.debug('LTI: lti_user_auth: %s' % lti_data)
    try:
        """ Check if user already exists using user., if not create new """
        user = User.objects.get(username=user_name)
        if settings.ALLOW_LMS_USER_INFO_SYNC:
            user.first_name = get_lti_value('lis_person_name_given', tool_provider)
            user.last_name = get_lti_value('lis_person_name_family', tool_provider)
            user.email = get_lti_value(settings.LTI_EMAIL, tool_provider)
            user.save()
    except User.DoesNotExist:
        """ first time entry, create new user """
        user = User.objects.create_user(user_name, email)
        user.set_unusable_password()
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()

    try:
        lti_user = LTIUser.objects.get(user=user)
    except Exception as e:
        logging.debug(e)
        lti_user = LTIUser.objects.create(user=user,
                                          lti_user_id=user_id,
                                          lti_lis_person_name_given=first_name,
                                          lti_lis_person_name_family=last_name,
                                          lti_lis_person_name_full=full_name,
                                          lti_lis_person_contact_email_primary=email)
    lti_user.save()

    lti_data['lti_user'] = lti_user

    user.backend = 'rooibos.auth.baseauth.BaseAuthenticationBackend'

    login(request, user)
    return True

#
#def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
#                   slug_separator='-'):
#    """
#    Calculates and stores a unique slug of ``value`` for an instance.
#
#    ``slug_field_name`` should be a string matching the name of the field to
#    store the slug in (and the field to check against for uniqueness).
#
#    ``queryset`` usually doesn't need to be explicitly provided - it'll default
#    to using the ``.all()`` queryset from the model's default manager.
#    """
#    slug_field = instance._meta.get_field(slug_field_name)
#
#    slug = getattr(instance, slug_field.attname)
#    slug_len = slug_field.max_length
#
#    # Sort out the initial slug, limiting its length if necessary.
#    slug = slugify(value)
#    if slug_len:
#        slug = slug[:slug_len]
#    slug = _slug_strip(slug, slug_separator)
#    original_slug = slug
#
#    # Create the queryset if one wasn't explicitly provided and exclude the
#    # current instance from the queryset.
#    if queryset is None:
#        queryset = instance.__class__._default_manager.all()
#    if instance.pk:
#        queryset = queryset.exclude(pk=instance.pk)
#
#    # Find a unique slug. If one matches, at '-2' to the end and try again
#    # (then '-3', etc).
#    next = 2
#    while not slug or queryset.filter(**{slug_field_name: slug}):
#        slug = original_slug
#        end = '%s%s' % (slug_separator, next)
#        if slug_len and len(slug) + len(end) > slug_len:
#            slug = slug[:slug_len-len(end)]
#            slug = _slug_strip(slug, slug_separator)
#        slug = '%s%s' % (slug, end)
#        next += 1
#
#    setattr(instance, slug_field.attname, slug)
#
#
#def _slug_strip(value, separator='-'):
#    """
#    Cleans up a slug by removing slug separator characters that occur at the
#    beginning or end of a slug.
#
#    If an alternate separator is used, it will also replace any instances of
#    the default '-' separator with the new separator.
#    """
#    separator = separator or ''
#    if separator == '-' or not separator:
#        re_sep = '-'
#    else:
#        re_sep = '(?:-|%s)' % re.escape(separator)
#    # Remove multiple instances and if an alternate separator is provided,
#    # replace the default '-' separator.
#    if separator != re_sep:
#        value = re.sub('%s+' % re_sep, separator, value)
#    # Remove separator from the beginning and end of the slug.
#    if separator:
#        if separator != '-':
#            re_sep = re.escape(separator)
#        value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
#    return value