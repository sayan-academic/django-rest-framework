# from django.shortcuts import render
# from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Avg
from rest_framework import status
from django.http import Http404
from rest_framework import generics, viewsets ,mixins
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication

# token authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import Product, Review
from .serializers import ProductSerializer, ReviewSerializer

# Create your views here.

# Token auth view
class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})

        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
        })
    
# Phase 5 code, ModelViewSet--epitome of DRY and simplicity.
# ReadOnlyModelViewSet exists for read only endpoints, it provides list and retrieve actions.
#Product
class ProductModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, 
                              SessionAuthentication, BasicAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            ismany = isinstance(kwargs["data"], list)
            kwargs["many"] = ismany
        return super().get_serializer(*args, **kwargs)
    
    # detail stands for detail view, basically a pk is mandatorily passed, therefore only for single products.
    # we are not updating the data, just retrieving for mathematical calc, therefore method is get.
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        product = self.get_object()

        aggregation_dict = product.reviews.aggregate(Avg('rating'))
        avg_rating = aggregation_dict['rating__avg']
        if avg_rating is None:
            status_label = "Unrated"
        elif float(avg_rating) > 3.0:
            status_label = "Good Product"
        else:
            status_label = "Bad Product"

        return Response({
            'product': product.name,
            'average rating': round(avg_rating, 2) if avg_rating else None,
            'status': status_label
        })  

#Review
class ReviewModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication, 
                              SessionAuthentication, BasicAuthentication]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            ismany = isinstance(kwargs["data"], list)
            kwargs["many"] = ismany
        return super().get_serializer(*args, **kwargs)
    
# Phase 4 code, GenericViewSet + mixins
'''
# Product
class ProductViewSet(viewsets.GenericViewSet,
                     mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            ismany = isinstance(kwargs["data"], list)
            kwargs["many"] = ismany
        return super().get_serializer(*args, **kwargs)
    
# Review 
class ReviewViewSet(viewsets.GenericViewSet,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            ismany = isinstance(kwargs["data"], list)
            kwargs["many"] = ismany
        return super().get_serializer(*args, **kwargs)
'''
# Phase 3 code, Concrete GenericAPIView
'''
#Product
class ProductGetPostGenericAPIview(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            ismany = isinstance(kwargs["data"], list)
            kwargs["many"] = ismany
        return super().get_serializer(*args, **kwargs)
class ProductGetPutDeleteGenericAPIview(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

#Review
class ReviewGetPostGenericAPIview(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            ismany = isinstance(kwargs["data"], list)
            kwargs["many"] = ismany
        return super().get_serializer(*args, **kwargs)
class ReviewGetPutDeleteGenericAPIview(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
'''
# Phase 2 code, GenericAPIView with mixins
'''
class ProductGetPostGenericAPIview(generics.GenericAPIView, 
                                   mixins.ListModelMixin,
                                   mixins.CreateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            is_many = isinstance(kwargs["data"], list)
            kwargs["many"] = is_many
        return super().get_serializer(*args, **kwargs)
    #hook perform_create to add custom logic before saving the object

class ProductGetPutDeleteGenericAPIview(generics.GenericAPIView,
                                        mixins.RetrieveModelMixin,
                                        mixins.UpdateModelMixin,
                                        mixins.DestroyModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class ReviewGetPostGenericAPIview(generics.GenericAPIView,
                                  mixins.ListModelMixin,
                                  mixins.CreateModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            ismany = isinstance(kwargs["data"], list)
            kwargs["many"] = ismany
        return super().get_serializer(*args, **kwargs)

class ReviewGetPutDeleteGenericAPIview(generics.GenericAPIView,
                                       mixins.RetrieveModelMixin,
                                       mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
'''
# Primitive Phase 1 code, APIview
'''
class ProductGetPostAPIview(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        is_many = isinstance(request.data, list)
        serializer = ProductSerializer(data=request.data, many=is_many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductGetUpdateDeleteAPIview(APIView):
    def getObject(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        product = self.getObject(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = self.getObject(pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = self.getObject(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewGetPostAPIview(APIView):
    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        is_many = isinstance(request.data, list)
        serializer = ReviewSerializer(data=request.data, many=is_many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ReviewGetUpdateDeleteAPIview(APIView):
    def getObject(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        review = self.getObject(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data)
    
    def put(self, request, pk):
        review = self.getObject(pk)
        serializer = ReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        review = self.getObject(pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''