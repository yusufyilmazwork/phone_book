from django.urls import path
from users import views



urlpatterns = [
    path('user-list', views.UserListView.as_view(), name='user_list'),
    path('edit-user', views.UserEditView.as_view(), name='edit_user'),
    path('delete-user', views.UserDeleteView.as_view(), name='delete_user'),
    path('user-detail', views.UserDetailView.as_view(), name='user_detail'),
    path('user-login', views.UserLoginView.as_view(), name='user_login'),
    path('user-register', views.UserRegisterView.as_view(), name='user_register'),
    path('change-password', views.ChangePasswordView.as_view(), name='change_password'),
    path('user-logout', views.UserLogoutView.as_view(), name='logout'),
    
]
