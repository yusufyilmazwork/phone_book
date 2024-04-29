from django.shortcuts import render
from students.models import Students, Courses, Teacher
from django.views.generic import ListView, CreateView
from students.forms import TeacherForm, StudentForm

# Create your views here.


class StudentsView(ListView):
    model = Students
    template_name = 'students/students-list.html'
    context_object_name = 'students'
    queryset = Students.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["schedule"] = Courses.objects.all()
        return context
    

class StudentsCreateView(CreateView):
    model = Students
    form_class = StudentForm
    template_name = "students/create-student.html"
    success_url = "../templates/index.html"

class TeacherListView(ListView):
    model = Teacher
    template_name = "students/teacher-list.html"
    context_object_name = "teachers"
    queryset = Students.objects.all()


class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = "students/create-teacher.html"
    success_url = "../templates/index.html"
