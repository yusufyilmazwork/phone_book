from rest_framework import serializers
from commers.models import Category, ImageModel, Brand, Product, Currency, Model, ModelPropertyValue, ModelPropertyKey
from users.models import ShoppingCartItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
        
class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageModel
        fields = '__all__'
        
        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ShoppingCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCartItem
        fields = ['id', 'product', 'model', 'amount']
        
class ProductPropertyKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPropertyKey
        fields = '__all__'
        

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'
        
        
class ModelPropertyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelPropertyValue
        fields = '__all__'
        
        
class ModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Model
        fields = ["title", "sku", "stock_amount", "in_box_quantity", "seq", "buying_price", "tax_rate", "product_id", "currency_id", "image_id", "is_active", "built_in"]

class ModelProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Model
        fields = ["title", "sku", "stock_amount", "in_box_quantity", "seq", "buying_price", "tax_rate", "product_id", "currency_id", "image_id", "is_active", "built_in"]


class ProductSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = ["title", "short_desc", "long_desc", "seq","image_id", "category_id","brand_id", "is_new", "is_featured", "is_active",  "built_in"]

class CategoryProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
        
class FeaturedProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'categories']        

class ReportSerializer(serializers.Serializer)  :
    categories = serializers.IntegerField()
    brands = serializers.IntegerField()
    products = serializers.IntegerField()
    offers = serializers.IntegerField()
    
    
class OfferReportSerializer(serializers.Serializer):
    period = serializers.CharField()
    totalProducts = serializers.IntegerField()
    totalAmount = serializers.DecimalField(max_digits=10, decimal_places=2)