from rest_framework import serializers
from .models import Product, Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model=Review
        fields = ['id', 'rating', 'content', 'product', 'created_at']

    # object level validation
    def validate(self, data):
        rating = data.get('rating')
        content = data.get('content')

        if rating==1 and len(content)<30:
            raise serializers.ValidationError({
                "content" : "1 star reviews must have 30 characters content."
            })
        return data

class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'reviews']
    # used validator in model Product

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