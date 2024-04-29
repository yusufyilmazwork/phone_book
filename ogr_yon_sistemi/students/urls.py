from django.urls import path
from students import views



urlpatterns = [
    path('students-list', views.StudentsView.as_view(), name='students_list'),
    path('/', views.StudentsView.as_view(), name='students_list'),
    path('create-student', views.StudentsCreateView.as_view(), name='create_student'),
    path('create-teacher', views.TeacherCreateView.as_view(), name='create_teacher'),

]
