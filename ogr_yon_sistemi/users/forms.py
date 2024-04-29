from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User

class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = forms.widgets.TextInput(attrs={"class": "form-control"})
        self.fields["password"].widget = forms.widgets.PasswordInput(attrs={"class": "form-control"})


class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget = forms.widgets.TextInput(attrs={"class": "form-control"})
        self.fields["email"].widget = forms.widgets.EmailInput(attrs={"class": "form-control"})
        self.fields["first_name"].widget = forms.widgets.TextInput(attrs={"class": "form-control"})
        self.fields["last_name"].widget = forms.widgets.TextInput(attrs={"class": "form-control"})
        self.fields["password1"].widget = forms.widgets.PasswordInput(attrs={"class": "form-control"})
        self.fields["password2"].widget = forms.widgets.PasswordInput(attrs={"class": "form-control"})
        self.fields["email"].required = True

    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email = email).exists():
            self.add_error("email", "bu email daha önce kullanılmış")

        return email
    

class UserPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget = forms.widgets.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password1"].widget = forms.widgets.PasswordInput(attrs={"class": "form-control"})
        self.fields["new_password2"].widget = forms.widgets.PasswordInput(attrs={"class": "form-control"})

class UserForm(forms.ModelForm):
    class Meta :
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
        labels = {
            "username": "Kullanıcı Adı",
            "email": "Email",
            "first_name": "Adı",
            "last_name": "Soyadı",
            "is_active": "Aktif mi?",
            "is_staff": "Çalışan mı?",
            "is_superuser": "Admin mi?"
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            "username": {
                "required": "Kullanıcı adı girmelisiniz",
                "max_length": "maksimum 100 karakter girmelisiniz"
            },
            "email": {
                "required": "Email bilgisi girmelisiniz"
            },
            "first_name": {
                "required": "Adı girmelisiniz",
                "max_length": "maksimum 100 karakter girmelisiniz"
            },
            "last_name": {
                "required": "Soyadı girmelisiniz",
                "max_length": "maksimum 100 karakter girmelisiniz"
            },
        }