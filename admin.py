from django.contrib import admin
from models import *
from django.contrib.contenttypes.models import ContentType
import logging


class GenericCollectionInlineModelAdmin(admin.options.InlineModelAdmin):
    ct_field = "content_type"
    ct_fk_field = "object_id"

    def __init__(self, parent_model, admin_site):
        logging.debug('GenericCollectionInlineModelAdmin init')
        super(GenericCollectionInlineModelAdmin, self).__init__(parent_model, admin_site)

        ctypes = ContentType.objects.all().order_by('id').values_list('id', 'app_label', 'model')
        elements = ["%s: '%s/%s'" % (id, app_label, model) for id, app_label, model in ctypes]

        self.content_types = "{%s}" % ",".join(elements)

    def get_formset(self, request, obj=None, **kwargs):
        result = super(GenericCollectionInlineModelAdmin, self).get_formset(request, obj)
        result.content_types = self.content_types
        result.ct_fk_field = self.ct_fk_field
        return result


class GenericCollectionTabularInline(GenericCollectionInlineModelAdmin):
    template = 'mdid-assignments/admin/edit_inline/gen_coll_tabular.html'


class GenericCollectionStackedInline(GenericCollectionInlineModelAdmin):
    template = 'mdid-assignments/admin/edit_inline/gen_coll_tabular.html'


class LTIUserAdmin(admin.ModelAdmin):
    raw_id_fields = ('user', )
    fields = ('lti_user_id',
              'lti_lis_person_name_given',
              'lti_lis_person_name_family',
              'lti_lis_person_contact_email_primary',)
    #inlines = ['CoursesTeachingInline', 'CoursesTakingInline', ]


class LTIObjectInline(admin.TabularInline):
    model = LTIObject


class CourseRosterInline(admin.TabularInline):
    model = CourseRoster


class InstructorInline(admin.StackedInline):
    model = LTIUser
    can_delete = False
    verbose_name_plural = 'instructors'


class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseRosterInline, InstructorInline, LTIObjectInline, ]


class SemesterAdmin(admin.ModelAdmin):
    pass


class PresentationAssignmentInline(admin.TabularInline):
    model = PresentationAssignment


class AssignmentSubmissionInline(admin.TabularInline):
    model = AssignmentSubmission


class AssignmentAdmin(admin.ModelAdmin):
    inlines = [AssignmentSubmissionInline,
               PresentationAssignmentInline, ]


class CourseLinkRelationInline(GenericCollectionInlineModelAdmin):
    model = CourseLinkRelation


class CourseLinkAdmin(admin.ModelAdmin):
    model = CourseLink
    inlines = [CourseLinkRelationInline, ]

    class Media:
        js = ('templates/admin/mdid-assignments/CustomRelatedObjectLookups.js',)

admin.site.register(LTIUser, LTIUserAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(CourseLink, CourseLinkAdmin)


