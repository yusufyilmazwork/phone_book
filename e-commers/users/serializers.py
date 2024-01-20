from rest_framework import serializers
from users.models import *
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import make_password
from commers.serializers import CurrencySerializer


class UserProfileLoginSerializer(serializers.Serializer):
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("username", "password")

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if (username is not None or password is not None):
            return attrs
        else:
            raise serializers.ValidationError(
                'Both email and password are required')

class UserRegisterSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    confirmPassword = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name",
                  "password", "confirmPassword", "email")

    def validate(self, attrs):
        if attrs.get("password") != attrs.get('confirmPassword'):
            raise serializers.ValidationError(
                {'password': 'Password fields did not match'})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def create(self, validated_data):
        if validated_data.get('password') != validated_data.get('confirmPassword'):
            raise serializers.ValidationError("Those password don't match")

        elif validated_data.get('password') == validated_data.get('confirmPassword'):
            validated_data['password'] = make_password(
                validated_data.get('password')
            )

        validated_data.pop('confirmPassword')
        return super(UserRegisterSerializer, self).create(validated_data)



class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        
        password_reset_form = PasswordResetForm(data=self.initial_data)
        if not password_reset_form.is_valid():
            raise serializers.ValidationError("Bu e-posta adresine sahip bir kullanıcı bulunamadı.")
        return value
    

class UserSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = User
        #fields = "__all__"
        exclude = ["last_login", "is_superuser", "email", "is_staff", "is_active", "date_joined"]

    

class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    old_password = serializers.CharField(write_only=True, required=True)
    confirmPassword = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'confirmPassword')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmPassword']:
            raise serializers.ValidationError({'password': 'Password fields did not match'})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"oldpassword": "Old password is not correct"})
        
    def update(self, instance, validated_data):
        user_pk = self.context['request'].user.pk
        password = validated_data.pop('password')
        if user_pk == instance.pk:
            instance.set_password(password)
            instance.save()
        return instance

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = "__all__"

        def get_userId(self, obj):
        
            return obj.user.id
        
                
        
class OfferItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferItem
        fields = '__all__'
        
        
        
class FavoritesSerliazer(serializers.ModelSerializer):
    class Meta:
        model = Favorites
        fields = ['id', 'product_id']


class OfferItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferItem
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class OfferSerializer(serializers.ModelSerializer):
    items = OfferItemSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    payments = CurrencySerializer(many=True, read_only=True)
    

    class Meta:
        model = Offer
        fields = '__all__'
class OfferAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

