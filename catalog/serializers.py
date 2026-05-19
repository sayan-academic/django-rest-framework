from rest_framework import serializers
from .models import Product, Review

#using HyperlinkedModelSerializer instead of ModelSerializer to use with Routers.
class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Review
        fields = ['url', 'id', 'rating', 'content', 'product', 'created_at']

    # object level validation   
    def validate(self, data):
        rating = data.get('rating')
        content = data.get('content')

        if rating==1 and len(content)<30:
            raise serializers.ValidationError({
                "content" : "1 star reviews must have 30 characters content."
            })
        return data

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    reviews = ReviewSerializer(many=True, read_only=True)

    status_url = serializers.HyperlinkedIdentityField(view_name='product-status')
    class Meta:
        model = Product
        fields = ['url', 'id', 'owner', 'name', 'description', 'price', 'status_url', 'reviews']
        read_only_fields = ['owner']
    # used validator in model Product
    def validate(self, data):
        price = data.get('price')

        if price <= 0:
            raise serializers.ValidationError({
                'price' : 'price has to be positive.'
            })
        return data
    
'''
class ReviewSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)   

    rating = serializers.ChoiceField(choices=Review.RatingChoices.choices, 
                                     default=Review.RatingChoices.STAR_5)
    content = serializers.CharField(style={'base_template': 'textarea.html'})
    created_at = serializers.DateTimeField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    
    def create(self, validated_data):
        return Review.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating', instance.rating)
        instance.content = validated_data.get('content', instance.content)
        instance.product = validated_data.get('product', instance.product)
        instance.save()
        return instance

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(style={'base_template': 'textarea.html'})
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    reviews = ReviewSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance
    
'''