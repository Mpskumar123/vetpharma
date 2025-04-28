from django.db import models

CATEGORY_CHOICES = [
    ('dog_food', 'Dog Food'),
    ('cat_food', 'Cat Food'),
    ('dog_medicine', 'Dog Medicine'),
    ('cat_medicine', 'Cat Medicine'),
]

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


#cart model
from django.db import models
from django.contrib.auth.models import User
from .models import Product

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    def total_price(self):
        return self.quantity * self.product.price
