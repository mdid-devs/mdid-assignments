from django import forms
from .models import Course, Instructor, Student, Semester, Assignment, PresentationAssignment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment


class PresentationAssignmentForm(forms.ModelForm):
    class Meta:
        model = PresentationAssignment
