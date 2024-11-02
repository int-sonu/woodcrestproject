from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Default role for superusers

        return self.create_user(email, username, password=password, **extra_fields)
        
class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('seller', 'Seller'),
        ('user', 'User'),  # Updated role name
    ]

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    pincode = models.CharField(max_length=6)
    address = models.TextField()
    password = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=True)  # Add this field for approval logic

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')  # Default role set to 'user'

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def is_admin(self):
        return self.role == 'admin'

    def is_seller(self):
        return self.role == 'seller'

    def is_user(self):
        return self.role == 'user'

from django.db import models

CATEGORY_STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
]

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=CATEGORY_STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name

SUBCATEGORY_STATUS_CHOICES = [
    (True, 'Active'),
    (False, 'Inactive'),
]

class SubCategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    sub_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True, choices=SUBCATEGORY_STATUS_CHOICES)

    def __str__(self):
        return self.sub_name
from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)  # Use string reference if Category is in the same file
    subcategory = models.ForeignKey('SubCategory', related_name='products', on_delete=models.CASCADE)  # Use string reference if SubCategory is in the same file
    wood = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)
    stock = models.IntegerField()
    description = models.TextField()
    additional_info = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sales_count = models.IntegerField(default=0)
    seller = models.ForeignKey('SellerProfile', on_delete=models.CASCADE)  # Use string reference for SellerProfile

    def __str__(self):
        return self.product_name

class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    alt_text = models.CharField(max_length=255, blank=True, null=True)

class Seat(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='seats')
    seat_type = models.CharField(max_length=50)
    seat_price = models.DecimalField(max_digits=10, decimal_places=2)


 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, default='Pending')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.product.product_name}'
    
    def get_items(self):
        return self.cartproduct_set.all()  
    def total_cost(self):
        return self.quantity * self.amount 
    
    
from django.db import models

class SellerProfile(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    password = models.CharField(max_length=255)
    business_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=15)
    business_pan_card = models.CharField(max_length=20)
    cheque_passbook_photo = models.ImageField(upload_to='documents/')
    sign = models.ImageField(upload_to='signatures/')
    account_holder_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=11)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True) 


    def __str__(self):
        return self.name
    
from django.db import models


class CustomCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    status = models.CharField(
        max_length=10, 
        choices=[('Active', 'Active'), ('Inactive', 'Inactive')], 
        default='Inactive'  # Set a default value for the status field
    )

    def __str__(self):
        return self.name


class CustomSubCategory(models.Model):
    category = models.ForeignKey(CustomCategory, related_name='custom_subcategories', on_delete=models.CASCADE)
    sub_name = models.CharField(max_length=255)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.sub_name

from django.db import models

class CustomRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    custom_requirements = models.TextField()
    image = models.ImageField(upload_to='custom_requests/', blank=True, null=True)

    def __str__(self):
        return self.username

from django.db import models

class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    rating = models.IntegerField()  # You can adjust the rating scale as needed, e.g., 1-5.
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment is created

    def __str__(self):
        return f"{self.name} - {self.rating}/5"
    
    from django.db import models
class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Reference to the Product model
    status = models.CharField(max_length=50, default='Pending')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)  # Adding quantity field to Orders


    def __str__(self):
        return f'Order {self.id} by {self.user.username} from seller {self.seller.name}'

# from django.db import models
# from django.contrib.auth.models import User

# class Payment(models.Model):
#     userw = models.ForeignKey(User, on_delete=models.CASCADE)
#     payment_id = models.CharField(max_length=255)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_method = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Payment {self.payment_id} for {self.user.username}"



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist - {self.product.product_name}"


from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


from django.db import models
from .models import User

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    address_line = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address_line}, {self.landmark if self.landmark else ''}, {self.city}, {self.district} - {self.pincode}"
