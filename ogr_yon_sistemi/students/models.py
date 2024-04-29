from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Teacher(models.Model):
    user = models.OneToOneField(User, related_name="teacher", on_delete=models.CASCADE)
    specialization = models.CharField(max_length=200)


    def __str__(self):
        return self.user.get_full_name
    

    class Meta:
        verbose_name="Ogretmen"
        verbose_name_plural="Ogretmenler"


    

class Courses(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, blank=True, null=True)
    schedule = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"{self.name}"


    class Meta:
        verbose_name='Kurs'
        verbose_name_plural = "Kurslar"

    

class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    teacher = models.ManyToManyField(Teacher, related_name="students")
    enrolled_course = models.ManyToManyField(Courses, related_name="student")
    note = models.FloatField(blank=True, null=True)
    lesson = models.ManyToManyField(Courses, related_name="students")


    def __str__(self):
        return f"{self.name} {self.surname}"


    class Meta:
        verbose_name='Ogrenci'
        verbose_name_plural = "Ogrenciler"


    



