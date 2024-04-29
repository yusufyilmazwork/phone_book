from django import forms
from students.models import Students, Teacher, Courses


class StudentForm(forms.ModelForm):
    class Meta:
        model = Students
        fields = "__all__"
        labels = {
            "user": "Ogrenci Adı",
            "birth_date": "Dogum Tarihi",
            "teacher": "Ogretmeni",
            "enrolled_course": "Kayıtlı Oldugu Kurs",
            "note": "Notu",
            "lesson": "Dersi"
        }
        widgets = {
            "user": forms.TextInput(attrs={"class": "form-control"}),
            "birth_date": forms.NumberInput(attrs={"class": "form-control"}),
            "teacher": forms.SelectMultiple(attrs={"class": "form-control"}),
            "enrolled_course": forms.SelectMultiple(attrs={"class": "form-control"}),
            "lesson": forms.SelectMultiple(attrs={"class": "form-control"}),
            "note": forms.NumberInput(attrs={"class": "form-control"}),
            
        }
        error_messages = {
            "user": {
                "required": "Zorunlu Alan",
                
            },
            "teacher": {
                "required": "Ogretmen Adını Seçmelisiniz.",
            },
            "enrolled_course": {
                "required": "Kayıtlı Kursu Secmelisiniz.",
            },
        }


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = "__all__"
        labels = {
            "user": "Ogretmen Adı",
            "specialization": "Branşı"
        }
        widgets = {
            "user": forms.TextInput(attrs={"class": "form-control"}),
            "specialization": forms.TextInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            "user": {
                "required": "İsim Zorunlu Alan",
            
            },
            "specialization": {
                "required": "Branş Zorunlu Alan",
            
            }
        }




class CoursesCreateForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = "__all__"
        labels = {
            "name": "Kurs İsmi",
            "code": "Kodu",
            "teacher": "Ogretmeni",
            "schedule": "Ders Programı"
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.NumberInput(attrs={"class": "form-control"}),
            "teacher": forms.SelectMultiple(attrs={"class": "form-control"}),
            "schedule": forms.TextInput(attrs={"class": "form-control"}),

        }
        error_messages = {
            "name": {
                "required": "Kurs İsmi Zorunlu Alan",
               
            },
            "code": {
                "required": "Kod Zorunlu Alan",
            }

        }
