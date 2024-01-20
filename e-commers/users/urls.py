from .views import *
from django.urls import path
from django.contrib.auth import views 
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)



urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(("user/<int:pk>"), UserListAPIView.as_view(), name="user_personal"),
    path(("user/admin/"), UserListAPIView.as_view(), name="user_all"),
    path(("user/<int:pk>/"), UserDetail.as_view(), name="user_detail"),
    path(("user/<int:pk>/admin/"), UserDetailAdminView.as_view(), name="user_detail_admin"),
    path(("cart/auth/"), ShoppingCartView.as_view(), name="cart_auth"),
    path(("favorites/auth/"), FavoritesView.as_view(), name="user_favorites"),
    path(("users/auth/"), AuthenticatedUserView.as_view(), name="user_auth"),
    
    #forget password
    
    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

     # Offers
    path('offers/admin/', AdminOffersView.as_view(), name='admin-offers'),
    path('offers/<int:pk>/admin', OfferAdminView.as_view(), name='offer-detail>'),
    path('offers/admin/user/<int:id>/', UserOffersView.as_view(), name='user-offers'),
    path('offers/auth/', OfferAuthView.as_view(), name='auth-user-offers'),
    path('offers/<int:id>/auth/', AuthUserOfferDetailView.as_view(), name='auth-user-offer-details'),
    path('offers/auth/create/', AuthUserOffersCreateView.as_view(), name='auth-user-offers-create'),
    path('offers/admin/<int:id>/', AdminOfferUpdateView.as_view(), name='admin-offer-update'),
]
