from django.contrib.auth.models import User
from django.db import models


# Admin Module
class AdminPanel(models.Model):
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_level = models.CharField(max_length=50, choices=[('Full', 'Full'), ('Limited', 'Limited')], default='Full')

    def __str__(self):
        return f"Admin: {self.admin_user.username} - {self.access_level}"


# User Management Module
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.img')
    address = models.TextField()
    phone = models.CharField(max_length=15)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# Product Management Module
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)  # Ensure this line is present

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name='product')
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name


# Cart and Checkout Module
class Cart(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} - {self.user.username}"


class Order(models.Model):
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"

# Create your models here.
