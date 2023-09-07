from django import forms
from .models import *

class PhoneBookForm(forms.ModelForm):
    class Meta:
        model = PhoneBook
        fields = ['ad', 'soyad', 'tel', 'email', 'image', 'adres', 'category']
        labels ={
            "ad":"İsim",
            "soyad":"Soyisim",
            "tel":"Telefon",
            "email":"Email",
            "image":"Kapak Fotografı",
            "adres":"Adres",
            "category":"Kategori",

        }
        widgets = {
            "ad": forms.TextInput(attrs={"class":"form-control"}),
            "soyad": forms.TextInput(attrs={"class":"form-control"}),
            "tel": forms.TextInput(attrs={"class":"form-control"}),
            "adres": forms.Textarea(attrs={"class":"form-control"}),
            "email": forms.TextInput(attrs={"class":"form-control"}),
            "category": forms.SelectMultiple(attrs={"class":"form-control"}),
        }

        error_messages = {
            "ad": {
                "required": "İsim alanı boş bırakılamaz.",
            },
            "soyad": {
                "required": "Soyisim alanı boş bırakılamaz.",
            },
            "tel": {
                "required": "Telefon alanı boş bırakılamaz.",
            },
            "category": {
                "required": "En az bir kategori secilmelidir.",
            },
            "image": {
                "required": "Fotograf yuklemeniz zorunludur",
            }


        }

class PhoneBookEditForm(forms.ModelForm):
            class Meta:
                model = PhoneBook
                fields = ['ad', 'soyad', 'tel', 'email', 'image', 'adres', 'category']
                labels ={
                    "ad":"İsim",
                    "soyad":"Soyisim",
                    "tel":"Telefon",
                    "email":"Email",
                    "image":"Kapak Fotografı",
                    "adres":"Adres",
                    "category":"Kategori",}
                
                widgets = {
                    "ad": forms.TextInput(attrs={"class":"form-control"}),
                    "soyad": forms.TextInput(attrs={"class":"form-control"}),
                    "tel": forms.TextInput(attrs={"class":"form-control"}),
                    "adres": forms.Textarea(attrs={"class":"form-control"}),
                    "email": forms.TextInput(attrs={"class":"form-control"}),
                    "category": forms.SelectMultiple(attrs={"class":"form-control"}),
            }

                error_messages = {
                    "ad": {
                        "required": "İsim alanı boş bırakılamaz.",
                    },
                    "soyad": {
                        "required": "Soyisim alanı boş bırakılamaz.",
                    },
                    "tel": {
                        "required": "Telefon alanı boş bırakılamaz.",
                    },
                    "category": {
                        "required": "En az bir kategori secilmelidir.",
                    },
                    "image": {
                "required": "Fotograf yuklemeniz zorunludur",
            }



        }


class CategoryCreateForm(forms.ModelForm):
     class Meta:
        model = Category
        fields = ["name"]
        labels ={
            "name":"Kategori İsmi",
           

        }
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),
            
        }

        error_messages = {
            "name": {
                "required": "Kategori alanı bos bırakılamaz.",
            },
        }


class CategoryEditForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = ("name",)
        labels ={
            "name":"Kategori İsmi",
          

        }
        widgets = {
            "name": forms.TextInput(attrs={"class":"form-control"}),

        }

        error_messages = {
            "name": {
                "required": "Kategori ismi boş bırakılamaz.",
            },
        }