from django import forms
from django.forms.extras.widgets import SelectDateWidget
from .models import Course, LTIUser, Semester, Assignment, PresentationAssignment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ('start', 'end', 'year')
        widgets = {
            'start': SelectDateWidget(),
            'end': SelectDateWidget(),
        }



class InstructorForm(forms.ModelForm):
    class Meta:
        model = LTIUser


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment


class PresentationAssignmentForm(forms.ModelForm):
    class Meta:
        model = PresentationAssignment
