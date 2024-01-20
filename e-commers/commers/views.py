from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, RetrieveDestroyAPIView
from commers.models import *
from users.models import Offer, ShoppingCartItem, Favorites, ShoppingCart
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from users.models import OfferItem
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .paginations import StandardResultsSetPagination
from datetime import datetime, timedelta
from django.db.models import Sum, Count
import datetime
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes



class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(is_active=1)
    serializer_class = CategorySerializer

    def get_queryset(self):
        
        if self.request.user.is_staff:
            return self.queryset.all()
        
        
        return self.queryset.filter(is_active=1)
    

class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        
        if instance.built_in:
            return Response({"detail": "Built-in categories cannot be updated."}, status=status.HTTP_400_BAD_REQUEST)

        
        if not instance.is_active and not request.user.is_staff:
            return Response({"detail": "Inactive categories cannot be updated."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

       
        if instance.built_in:
            return Response({"detail": "Built-in categories cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)

       
        if Product.objects.filter(category=instance).exists():
            return Response({"detail": "The category has related records in the products table and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()

        return Response({"detail": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class CategoryProductsView(ListAPIView):
    serializer_class = CategoryProductSerializer
    
    def get_queryset(self):
        category_id = self.kwargs.get("pk")
        return Category.objects.filter(id=category_id, is_active=1)
    
   
class ImageModelListView(ListCreateAPIView):
    queryset = ImageModel.objects.all()
    serializer_class = ImageModelSerializer
    
   
class ImageModelDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ImageModel.objects.all()
    serializer_class = ImageModelSerializer
    

class BrandListView(ListCreateAPIView):
    serializer_class = BrandSerializer

    def get_queryset(self):
        
        if self.request.user.is_staff:
            return Brand.objects.all()
        

        return Brand.objects.filter(is_active=1)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class BrandDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        
        if instance.built_in:
            return Response({"detail": "Built-in brands cannot be updated."}, status=status.HTTP_400_BAD_REQUEST)

        
        if not instance.is_active and not request.user.is_staff:
            return Response({"detail": "Inactive brands cannot be updated."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

       
        if instance.built_in:
            return Response({"detail": "Built-in brands cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)

        if Product.objects.filter(brand=instance).exists():
            return Response({"detail": "The brand has related records in the products table and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)

        instance.delete()

        return Response({"detail": "Brand deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    


class CartAuthView(APIView):
    @permission_classes([IsAuthenticated])
    def get(self, request):
        
        cart = ShoppingCart.objects.get(user_id=request.user)
        cart_items = ShoppingCartItem.objects.filter(cart=cart)
        serializer = ShoppingCartItemSerializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        model_id = request.data.get('model_id')
        amount = request.data.get('amount')

        
        cart, created = ShoppingCart.objects.get_or_create(user_id=request.user)

       
        cart_item, created = ShoppingCartItem.objects.get_or_create(cart=cart, model_id=model_id)

       
        if amount == 0:
            cart_item.delete()
            return Response({"detail": "Cart item deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            cart_item.amount = amount
            cart_item.save()
            serializer = ShoppingCartItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)








class ProductPropertyKeyListView(ListAPIView):
    queryset = ModelPropertyKey.objects.all()
    serializer_class = ProductPropertyKeySerializer
    

class CurrencyListView(ListCreateAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
    

class ModelPropertyValueListView(ListAPIView):
    queryset = ModelPropertyValue.objects.all()
    serializer_class = ModelPropertyValueSerializer
    

class ModelCreateView(CreateAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    
    # def create(self, request, *args, **kwargs):
    #     data = request.data.copy()
        
    #     data['create_at'] = datetime.datetime.now()
        
    #     sku = data.get('sku')
    #     if sku and Model.objects.filter(sku=sku).exists():
    #         return Response({'error': 'SKU already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     serializer = self.get_serializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
        
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class ModelListView(ListAPIView):
    serializer_class = ModelProductSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('pk')
        queryset = Model.objects.filter(product_id=product_id)

        if self.request.user.is_staff:
            return queryset
        
        queryset = queryset.filter(is_active=1)
        return queryset
    

class ModelDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Model.objects.all()
    serializer_class = ModelSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.built_in:
            return Response({"error": "Built-in models cannot be updated."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.built_in:
            return Response({"error": "Built-in models cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)
        
        if OfferItem.objects.filter(product__model=instance).exists():
            return Response({"error": "Model has related records in offer_items table and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        
        ModelPropertyValue.objects.filter(model=instance).delete()
        ShoppingCartItem.objects.filter(model=instance).delete()

        instance.delete()

        return Response({"detail": "Model deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    
    
    

class ProductListView(ListCreateAPIView):
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    queryset = Product.objects.filter(is_active=True)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(title__icontains=q)
        return queryset


class ProductDetailView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.builtIn:
            raise serializers.ValidationError("Built-in products cannot be updated.")


class ProductDeleteView(RetrieveDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

     
        if instance.built_in:
            return Response({"detail": "Built-in products cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)

        if OfferItem.objects.filter(product=instance).exists():
            return Response({"detail": "The product has related records in offer_items table and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)


        Model.objects.filter(product=instance).delete()
        ModelPropertyKey.objects.filter(product=instance).delete()
        ShoppingCartItem.objects.filter(product=instance).delete()
        Favorites.objects.filter(product=instance).delete()

        instance.delete()

        return Response({"detail": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)



# class ProductDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
    
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
        
#         if instance.built_in:
#             return Response({"error": "Built-in products cannot be updated."}, status=status.HTTP_403_FORBIDDEN)
        
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
        
#         return Response(serializer.data)
    
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
        
#         if instance.built_in:
#             return Response({"error": "Built-in products cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)
        
#         if OfferItem.objects.filter(product=instance).exists():
#             return Response({"error": "Product has related records in offer_items table and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)

#         self.perform_destroy(instance)
#         return Response({'id': instance.id, 'title': instance.title})
    

class FeatueredProductListView(ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.filter(is_featured=True)
    

class ProductPropertiesCreateView(CreateAPIView):
    serializer_class = ProductPropertyKeySerializer
    
    @action(detail=False, methods=['post'])
    def create_property(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductPropertiesCreateView(CreateAPIView):
    queryset = ModelPropertyKey.objects.all()
    serializer_class = ProductPropertyKeySerializer

    def create(self, request, *args, **kwargs):
        # Varsayılan builtIn değeri
        request.data['builtIn'] = False

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ProductPropertiesListView(ListAPIView):
    serializer_class = ProductPropertyKeySerializer
    queryset = ModelPropertyKey.objects.all()
    
    @action(detail=True, methods=['get'])
    def properties(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        
        property_keys = ModelPropertyKey.objects.filter(product=product)
        serializer = self.get_serializer(property_keys, many=True)
        return Response(serializer.data)
    

class ProductPropertiesDetailView(RetrieveUpdateDestroyAPIView):
    queryset = ModelPropertyKey.objects.all()
    serializer_class = ProductPropertyKeySerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.built_in:
            return Response({"error": "Built-in products cannot be updated."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        
        if instance.built_in:
            return Response({"error": "Built-in products cannot be deleted."}, status=status.HTTP_403_FORBIDDEN)
        
        related_records = instance.modelpropertyvalue_set.all()
        if related_records.exists():
            return Response({"error": "Product has related records in model_property_value table and cannot be deleted."}, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_destroy(instance)
        return Response({'id': instance.id, 'name': instance.name})
    

# ---------- Report ----------
# Report View
class ReportView(RetrieveAPIView):
    serializer_class = ReportSerializer
    
    def get_object(self):
        today = datetime.datetime.now()
        categories_count = Category.objects.filter(is_active=1).count()
        brands_count = Brand.objects.filter(is_active=1).count()
        products_count = Product.objects.filter(is_active=1).count()
        offers_total = Offer.objects.filter(create_at__date=today).count()
        
        data = {
            'categories': categories_count,
            'brands': brands_count,
            'products': products_count,
            'offers': offers_total
        }
        
        return data
    
# Offer Report View
class OfferReportView(ListAPIView):
    serializer_class = OfferReportSerializer
    
    def get_queryset(self):
        date1 = self.request.query_params.get('date1')
        date2 = self.request.query_params.get('date2')
        report_type = self.request.query_params.get('type')
        
        if date1 and date2 and report_type:
            date1 = datetime.strptime(date1, '%Y-%m-%d')
            date2 = datetime.strptime(date2, '%Y-%m-%d')
            
            if report_type == 'day':
                period = timedelta(days=1)
            elif report_type =='week':
                period = timedelta(weeks=1)
            elif report_type == 'month':
                period = timedelta(days=30)
            elif report_type == 'year':
                period = timedelta(days=365)
            
            queryset = []
            current_date = date1
            while current_date <= date2:
                next_date = current_date + period
                total_products = Offer.objects.filter(created_at__gte=current_date, created_at__lt=next_date).count()
                total_amount = Offer.objects.filter(created_at__gte=current_date, created_at__lt=next_date).aggregate(total_amount=Sum('amount'))['amount__sum'] or 0
                
                report_entry = {
                    'period': current_date.strftime('%b %Y'),
                    'totalProducts': total_products,
                    'totalAmount': total_amount
                }
                
                queryset.append(report_entry)
                
                current_date = next_date
                
            return queryset
        
        else:
            return Offer.objects.none()
        
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        if queryset is not None:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid parameters'}, status=status.HTTP_400_BAD_REQUEST)
    
# Most Popular Products Report View
class MostPopularProductsView(ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        amount = self.request.query_params.get('amount')
        if amount is not None and amount.isnumeric():
            return Product.objects.annotate(num_offers=Count('offer')).order_by('-num_offers')[:int(amount)]
        return Product.objects.none()
    
# Unoffered Product View
class UnofferedProductView(ListAPIView):
    serializer_class = ProductSerializer
    
    def get_queryset(self):
        return Product.objects.filter(is_active=False)