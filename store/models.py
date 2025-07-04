from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('MANAGER', 'Manager'),
        ('STAFF', 'Staff'),
        ('CUSTOMER', 'Customer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='CUSTOMER')
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    old_cart = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance, role='CUSTOMER')
        user_profile.save()

post_save.connect(create_profile, sender=User)

class Customer(models.Model):
    fisrt_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=200, null=True)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    Sale_price = models.FloatField()
    description = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    Is_sale = models.BooleanField(default=False, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0, help_text="Available stock quantity")
    
    def __str__(self):
        return self.name
    
    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.quantity > 0
    
    @property
    def stock_status(self):
        """Get stock status as string"""
        if self.quantity == 0:
            return "Out of Stock"
        elif self.quantity <= 5:
            return f"Low Stock ({self.quantity} left)"
        else:
            return f"In Stock ({self.quantity} available)"
    
    def has_sufficient_stock(self, requested_quantity):
        """Check if there's sufficient stock for the requested quantity"""
        return self.quantity >= requested_quantity
    
    def reduce_stock(self, quantity):
        """Reduce stock by the specified quantity"""
        if self.has_sufficient_stock(quantity):
            self.quantity -= quantity
            self.save()
            return True
        return False
    
    def add_stock(self, quantity):
        """Add stock by the specified quantity"""
        self.quantity += quantity
        self.save()

class Order(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return str(self.Product)