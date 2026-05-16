from django.db import models
from django.core.validators import MaxValueValidator

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    # VALIDATOR
    price = models.DecimalField(max_digits=10, 
                                decimal_places=2,
                                validators=[MaxValueValidator(50000.00)])

    def __str__(self):
        return f"{self.name} added, price = {self.price}"

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')

    class RatingChoices(models.IntegerChoices):
        STAR_1 = 1, "1 Star"
        STAR_2 = 2, "2 Star"
        STAR_3 = 3, "3 Star"
        STAR_4 = 4, "4 Star"
        STAR_5 = 5, "5 Star"
    rating = models.IntegerField(choices=RatingChoices, default=5)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    