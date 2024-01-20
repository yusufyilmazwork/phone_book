from django.shortcuts import render
from rest_framework_simplejwt.tokens import  RefreshToken
from .models import User, ShoppingCartItem, ShoppingCart
from commers.models import Product
from .serializers import *
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework import filters
import math
from core.page_filter import pages_filter
from django.contrib.auth.views import PasswordResetView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from django.core.mail import send_mail
from datetime import datetime
from rest_framework.decorators import permission_classes
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

class UserLoginView(ListAPIView):
    serializer_class = UserProfileLoginSerializer
    queryset = User.objects.all()
    def post(self, request):
        serializer = UserProfileLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                return Response({'access_token': access_token}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Kullanıcı adı veya şifre yanlış.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(data, status=status.HTTP_201_CREATED)
    
    def validate(self, attrs):
        if attrs.get("password") != attrs.get('confirmPassword'):
            raise serializers.ValidationError(
                {'password': 'Password fields did not match'})
        if attrs.get("email") is None:
            raise serializers.ValidationError(
                {'email': 'Email field cannot be empty'})
        if attrs.get("username") is None:
            raise serializers.ValidationError(
                {'username': 'Username field cannot be empty'})
        
        return attrs


class PasswordResetAPIView(CreateAPIView):
    serializer_class = PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Parola sıfırlama e-postası gönderme işlemi
            PasswordResetView.as_view()(request)
            return Response({"message": "Parola sıfırlama bağlantısı e-posta adresinize gönderildi."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["first_name", "email"]
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        queryset = User.objects.all()

        if self.request.path == '/users/user/':
            return User.objects.filter(id=self.request.user.id)
        else:
            return queryset
        
    def list(self, request, *args, **kwargs):
        if request.path.startswith('/users/user/') or request.path.startswith('/users/user'):
            return pages_filter(self, request, User, *args, **kwargs)
        return super().list(request, *args, **kwargs)
    
    

class UserDetailAdminView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserDetail(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ChangePasswordView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return self.request.user
    
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        data = super().update(request, *args, **kwargs)
        return Response({"update": "successful", "success": True})


class ShoppingCartView(RetrieveUpdateDestroyAPIView):
    
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]
    

    def get_object(self):
        return ShoppingCart.objects.get(user=self.request.user)
    
    


class FavoritesView(RetrieveUpdateDestroyAPIView):
    serializer_class = FavoritesSerliazer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return Favorites.objects.get(user=self.request.user)
    
class AuthenticatedUserView(APIView):
    
    @permission_classes([IsAuthenticated])
    def get(self, request):
        user = request.user
        user_data = {
            "id": user.id,
            "firstName": user.first_name,
            # Add other user attributes as needed
        }
        return JsonResponse(user_data)

    @permission_classes([IsAuthenticated])
    def put(self, request):
        user = request.user

        if user.builtIn:
            return JsonResponse({"detail": "Built-in users cannot be updated."}, status=status.HTTP_400_BAD_REQUEST)

        # Implement user update logic here (use your serializer)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        user = request.user
        form = PasswordChangeForm(user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important for maintaining user's session
            return JsonResponse({"detail": "Password updated successfully."})
        else:
            return JsonResponse(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @permission_classes([IsAuthenticated])
    def delete(self, request):
        user = request.user

        if user.builtIn:
            return JsonResponse({"detail": "Built-in users cannot be updated."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user has related records in offers table
        if Offer.objects.filter(user=user).exists():
            return JsonResponse({"detail": "Cannot delete user with related records in offers table."}, status=status.HTTP_400_BAD_REQUEST)

        user.delete()
        return JsonResponse({"detail": "User deleted successfully."})





# ---------- Offers Views ----------    

class AdminOffersView(ListAPIView):
   
    serializer_class = OfferSerializer
    #filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    def get_queryset(self):
        queryset = Offer.objects.all()
        q = self.request.query_params.get('q', '')
        status = self.request.query_params.get('status', '')
        date1 = self.request.query_params.get('date1', '')
        date2 = self.request.query_params.get('date2', '')
        
        if q:
            queryset = queryset.filter(Q(code__icontains=q) | Q(user__first_name__icontains=q) | Q(user__last_name__icontains=q))
        if status:
            queryset = queryset.filter(status=status)
        if date1:
            queryset = queryset.filter(create_at__gte=date1)
        if date2:
            queryset = queryset.filter(create_at__lte=date2)

        return queryset

class OfferAdminView(RetrieveUpdateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferAdminSerializer

    @permission_classes([IsAdminUser])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @permission_classes([IsAdminUser])
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)



class UserOffersView(ListAPIView):
    serializer_class = OfferSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('id')
        status = self.request.query_params.get('status', '')
        date1 = self.request.query_params.get('date1', '')
        date2 = self.request.query_params.get('date2', '')
        page = self.request.query_params.get('page', 1)
        size = self.request.query_params.get('size', 10)
        sort = self.request.query_params.get('sort', 'create_at')
        sort_type = self.request.query_params.get('type', 'desc')

        offers = Offer.objects.filter(user_id=user_id)

        if status:
            offers = offers.filter(status=status)

        if date1 and date2:
            offers = offers.filter(create_at__range=[date1, date2])

        if sort_type == 'desc':
            offers = offers.order_by(f'-{sort}')
        else:
            offers = offers.order_by(sort)

        start = (page - 1) * size
        end = start + size
        offers = offers[start:end]

        return offers


class OfferAuthView(APIView):

    def get(self, request):
        q = request.query_params.get('q', '')
        date1 = request.query_params.get('date1', '')
        date2 = request.query_params.get('date2', '')
        status = request.query_params.get('status', '')
        page = request.query_params.get('page', 0)
        size = request.query_params.get('size', 20)
        sort = request.query_params.get('sort', 'loanDate')
        type = request.query_params.get('type', 'desc')

        if date1:
            date1 = datetime.strptime(date1, '%Y-%m-%d %H:%M:%S')
        if date2:
            date2 = datetime.strptime(date2, '%Y-%m-%d %H:%M:%S')
    
        offers = Offer.objects.filter(user=request.user, code__icontains=q, create_at__gte=date1, create_at__lte=date2, status=status)
        
        offers = offers.order_by(sort if type == 'asc' else '-' + sort)
        
        start = int(page) * int(size)
        end = start + int(size)
        offers = offers[start:end]

        serializer = OfferSerializer(offers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        
        offer = Offer.objects.create(user=request.user)
        
        # Burada teklifin kodunu ve diğer hesaplamaları yapabilirsiniz
        # Örneğin, kod oluşturma ve grand total hesaplama işlemleri burada gerçekleşebilir.
        
        # OfferItem'ları ekleyin
        items = request.data.get('items', [])
        for item_data in items:
            product_id = item_data.get('product_id')
            amount = item_data.get('amount')
            
            product = Product.objects.get(id=product_id)
            
            
            product.stock_amount -= 1
            product.save()
            
            
            item = OfferItem.objects.create(offer=offer, product=product, amount=amount)
        
        
        user_email = request.user.email
        sales_specialist_email = "sales_specialist@example.com"  
        
        send_mail(
            'Yeni Teklif Oluşturuldu',
            'Yeni bir teklif oluşturuldu. Teklif numarası: {}'.format(offer.code),
            'your_email@example.com',  # Gönderen e-posta adresi
            [user_email, sales_specialist_email],
            fail_silently=False,
        )
        
        
        serializer = OfferSerializer(offer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class AuthUserOfferDetailView(RetrieveAPIView):
    serializer_class = OfferSerializer
    


    def get_queryset(self):
        user = self.request.user
        offer_id = self.kwargs.get('id')

        try:
            offer = Offer.objects.get(id=offer_id, user_id=user)
            return [offer]
        except Offer.DoesNotExist:
            return []
        

class AuthUserOffersCreateView(CreateAPIView):
    serializer_class = OfferSerializer
    
    # def get_queryset(self):
    #     user_id = self.request.user.id
    #     currency_id = self.request.data.get('currency_id')
    #     return Offer.objects.filter(user_id=user_id, currency_id=currency_id)
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return response
    

class AdminOfferUpdateView(UpdateAPIView):
    serializer_class = OfferSerializer
    
    def get_queryset(self):
        offer_id = self.kwargs.get('id')
        user = self.request.user
        
        try:
            offer = Offer.objects.get(id=offer_id)
            if user.userprofile.role_set.filter(role_name__in=['Sales Specialist', 'Admin']).exists():
                return [offer]
        except Offer.DoesNotExist:
            return []
        
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        return response