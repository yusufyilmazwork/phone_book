from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.urls import reverse_lazy
from .models import UserProfile
from users.forms import LoginUserForm, NewUserForm, UserPasswordChangeForm, UserForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import FormView
from django.views.generic import RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView, DeleteView, DetailView

# Create your views here.

class UserListView(ListView):
    model = UserProfile
    template_name = "users/user-list.html"
    context_object_name = "users"

class UserEditView(UpdateView):
    model = UserProfile
    template_name = "users/edit-user.html"
    form_class = UserForm
    context_object_name = "user"
    success_url = "/users/user-list/"
    pk_url_kwarg = "user_id"

class UserDeleteView(DeleteView):
    model = UserProfile
    template_name = "users/user-delete.html"
    context_object_name = "user"
    success_url = "/users/user-list/"
    pk_url_kwarg = "user_id"


class UserDetailView(DetailView):
    model = UserProfile
    template_name = "users/user-detail.html"
    context_object_name = "user"
    pk_url_kwarg = "user_id"





class UserLoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginUserForm
    success_url = "user-list"
    login_url = "/users/login"

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, "Giriş Başarılı")
            return super().form_valid(form)
        else:
            messages.add_message(self.request, messages.ERROR, "Kullanıcı adı veya şifre hatalı")
            return self.form_invalid(form)

class UserRegisterView(SuccessMessageMixin, FormView):
    template_name = "users/register.html"
    form_class = NewUserForm
    success_url = "../templates/index.html"
    success_message = "Kayıt işlemi başarıyla tamamlandı"

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        user = authenticate(self.request, username=username, password=password)
        login(self.request, user)
        return super().form_valid(form)

    

class ChangePasswordView(LoginRequiredMixin, FormView):
    template_name = "users/change-password.html"
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("change_password")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        user = form.save()
        update_session_auth_hash(self.request, user)
        messages.success(self.request, "Parolanız Güncellendi!")
        return super().form_valid(form)



class UserLogoutView(RedirectView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "Çıkış Başarılı")
        return redirect(reverse_lazy("books_index"))
    
