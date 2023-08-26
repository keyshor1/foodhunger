from django.db import models
from app.models import *

# Create your models here.

class Cabin(models.Model):
    cabinnumber = models.CharField(max_length=200)
    photo = models.ImageField(upload_to="cabinimage")
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.cabinnumber)


class Cabinorder(models.Model):
    cabin = models.ForeignKey(Cabin,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) 
    
    def __str__(self):
        return self.product.title
    
    # @property
    # def total_cost(self):
    #     return self.quantity * self.product.discounted_price


STATUS_CHOICES = {
    ('Pending','Pending'),
    ('Cash','Cash'),
    ('Online Payment','Online Payment'),
    ('Credit','Credit'),
}


class Billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cabin = models.ForeignKey(Cabin, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Use DecimalField for currency
    billing_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return str(self.cabin)
