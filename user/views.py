from django.shortcuts import render
from django.http import Http404
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
import jwt
from ananas.settings import SECRET_KEY
from rest_framework_simplejwt import exceptions

from .models import Vendor, Customer
from .permissions import AnonPermissionOnly, IsOwnerOrReadOnly
from .serializers import (
    MyTokenObtainPairSerializer,
    VendorRegisterSerializer,
    CustomerRegisterSerializer,
    VendorSerializer,
    VendorProfileSerializer,
    CustomerSerializer,
)
from product.models import Product, Cart
from product.serializers import ProductSerializer, CartSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response



def decode_auth_token(token):
    try:
        user = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        msg = 'Signature has expired. Login again'
        raise exceptions.AuthenticationFailed(msg)
    except jwt.DecodeError:
        msg = 'Error decoding signature. Type valid token'
        raise exceptions.AuthenticationFailed(msg)
    except jwt.InvalidTokenError:
        raise exceptions.AuthenticationFailed()
    return user


class LoginView(TokenObtainPairView):
    permission_classes = (AnonPermissionOnly,)
    serializer_class = MyTokenObtainPairSerializer


class VendorRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VendorRegisterSerializer(data=request.data)
        if serializer.is_valid():
            vendor = Vendor.objects.create(
                email=request.data['email'],
                name=request.data['name'],
                second_name=request.data['second_name'],
                phone_number=request.data['phone_number'],
                description=request.data['description'],
                is_Vendor=True
            )
            vendor.set_password(request.data['password'])
            vendor.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_REQUEST)


class CustomerRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CustomerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            customer = Customer.objects.create(
                email=request.data['email'],
                name=request.data['name'],
                second_name=request.data['second_name'],
                phone_number=request.data['phone_number'],
                card_number=request.data['card_number'],
                address=request.data['address'],
                post_code=request.data['post_code'],
                is_Vendor=False
            )
            customer.set_password(request.data['password'])
            customer.save()
            cart = Cart.objects.create(
                customer=customer 
            )
            cart.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorQuantityView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        vendors = Vendor.objects.filter(is_Vendor=True)
        vendor_count = vendors.count()
        data = {'vendor_count': vendor_count}
        return Response(data)


class CustomerQuantityView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        customers = Customer.objects.all()
        customer_count = customers.count()
        data = {'customer_count': customer_count}
        return Response(data)


class VendorListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        vendors = Vendor.objects.filter(is_Vendor=True) # Получаем все записи продавцов
        serializer = VendorSerializer(vendors, many=True) # Сериализуем записи
        return Response(serializer.data)


class CustomerListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        vendors = Customer.objects.all()
        serializer = CustomerRegisterSerializer(vendors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class CustomerProfileView(APIView):
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
#
#     def get(self, request, id):
#         customer = Customer.objects.get(id=id)
#         serializer = CustomerRegisterSerializer(customer)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class VendorProfileView(APIView):
#     permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
#
#     def get(self, request, id):
#         customer = Vendor.objects.get(id=id)
#         serializer = VendorRegisterSerializer(customer)
#         return Response(serializer.data, status=status.HTTP_200_OK)


class VendorProfileView(APIView):
    permission_classes = [permissions.AllowAny]

    # def get_object(self, token):
    #     try:
    #         user = decode_auth_token(token)
    #         return Vendor.objects.get(id=user['user_id'])
    #     except Vendor.DoesNotExist:
    #         raise Http404
    #
    # def get(self, request, token):
    #     vendor = self.get_object(token)
    #     products = Product.objects.filter(vendor=vendor)
    #     vendor_data = VendorProfileSerializer(vendor).data
    #     product_data = ProductSerializer(products, many=True).data
    #     vendor_data['products'] = product_data
    #     return Response(vendor_data)

    def get_object(self, token):
        try:
            user = decode_auth_token(token)
            return Vendor.objects.get(id=user['user_id'])
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, token):
        snippet = self.get_object(token)
        products = Product.objects.filter(vendor=snippet)
        serializer = VendorProfileSerializer(snippet).data
        serializer2 = ProductSerializer(products, many=True).data
        serializer['products'] = serializer2
        return Response(serializer)

    def put(self, request, token):
        snippet = self.get_object(token)
        serializer = VendorProfileSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, token):
        snippet = self.get_object(token)
        snippet.delete()
        return Response(status.HTTP_204_NO_CONTENT)


class VendorDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, id):
        try:
            return Vendor.objects.get(id=id)
        except Vendor.DoesNotExist:
            raise Http404

    def get(self, request, id):
        snippet = self.get_object(id)
        products = Product.objects.filter(vendor_id=id)
        serializer = VendorRegisterSerializer(snippet)
        serializer2 = ProductSerializer(products, many=True)
        data = serializer.data
        data['products'] = serializer2.data
        return Response(data, status=status.HTTP_200_OK)


class CartView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, user_id):
        try:
            return Cart.objects.get(customer_id=user_id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, user_id):
        cart = self.get_object(user_id)
        serializer = CartSerializer(cart)
        prod_serializer = ProductSerializer(cart.product.all(), many=True)
        user_serializer = CustomerRegisterSerializer(cart.customer)
        data = serializer.data
        data['customer'] = user_serializer.data
        data['product'] = prod_serializer.data
        return Response(data, status=status.HTTP_200_OK)


class AddToCartView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, user_id):
        try:
            return Cart.objects.get(customer_id=user_id)
        except Product.DoesNotExist:
            raise Http404

    def put(self, request, user_id):
        cart = self.get_object(user_id)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)