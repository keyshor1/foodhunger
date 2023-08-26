from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

STATE_CHOICES = (
    ('Damak 1', 'Damak 1'),
    ('Damak 2', 'Damak 2'),
    ('Damak 3', 'Damak 3'),
    ('Damak 4', 'Damak 4'),
    ('Damak 5', 'Damak 5'),
    ('Damak 6', 'Damak 6'),
    ('Damak 7', 'Damak 7'),
)

CATEGORY_CHOICES=(
    ('BF','Breakfast'),
    ('LH','Lunch'),
    ('DN','Dinner'),
    ('DT','Desert'),
    ('DR','Drinks'),
    ('PT','Platter'),
    ('FF','Fast Food'),
    ('PD','Popular Dishes'),
    ('NA', 'New Arrivals')
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    def __str__(self):
        return str(self.title)


class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=100)
    def __str__(self):
        return str(self.id)
    

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) 
    
    def __str__(self):
        return str(self.product)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = {
    ('Pending','Pending'),
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel'),
}

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES, default='Pending')
    def __str__(self):
        return str(self.id)
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.TextField(max_length=50)
    comment = models.TextField(max_length=200)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('accepted', 'Accepted'),
            ('pending', 'Pending'),
            ('declined', 'Declined')
        ],
        default='pending'
    )

    def __str__(self):
        return str(self.id)
    
Custom_Status = (
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Declined', 'Declined'),
)

class Custom_Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to="myimage")
    phonenumber = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    custom_status = models.CharField(max_length=50, choices=Custom_Status, default='Pending')
    customchoices = models.TextField(max_length=200, default='')
    def __str__(self):
        return self.product.title
    
class Viva(models.Model):
    studentname = models.CharField(max_length=55)
    studentmarks = models.IntegerField(default=0)
    def __str__(self):
        return str(self.studentname)
    
