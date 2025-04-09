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
        ('user', 'User'),  
        ('delivery_agent', 'Delivery Agent'),  # Added Delivery Agent role
        ('designer', 'Designer'),  # Added Designer role
    ]

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    mobile_number = models.CharField(max_length=15)
    pincode = models.CharField(max_length=6)
    address = models.TextField()
    password = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=True)  

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('blocked', 'Blocked'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')  

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

    def is_delivery_agent(self):
        return self.role == 'delivery_agent'  # Added method for Delivery Agent role
    
    def is_designer(self):
        return self.role == 'designer'  # Added method for Designer role
    
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
    seller = models.ForeignKey(User, on_delete=models.CASCADE)  # Use string reference for SellerProfile

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


class CustomRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    custom_requirements = models.TextField()
    image = models.ImageField(upload_to='custom_requests/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    updated_at = models.DateTimeField(auto_now=True)  # Tracks last update

    def __str__(self):
        return f"{self.user.username} - {self.status}"


from django.db import models

class Comment(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    rating = models.IntegerField()  # You can adjust the rating scale as needed, e.g., 1-5.
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment is created

    def __str__(self):
        return f"{self.name} - {self.rating}/5"
    

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
    
    
    

class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, null=True, blank=True)
    payment_method = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  
    status = models.CharField(max_length=50, default='Pending')
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)  


    def __str__(self):
        return f'Order {self.id} by {self.user.username} from seller {self.seller.name}'


class DeliveryAgent(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')  
    vehicle_type = models.CharField(max_length=100)
    vehicle_id = models.CharField(max_length=50, unique=True)
    delivery_area = models.CharField(max_length=255)
    address = models.TextField()
    preferred_working_hours = models.CharField(max_length=100)
    emergency_contact = models.CharField(max_length=15)
    bank_details = models.TextField()
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True, null=True)
    id_proof = models.FileField(upload_to="id_proofs/", blank=True, null=True)
    is_approved = models.BooleanField(default=False)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_completed = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    available = models.BooleanField(default=True)  # Maybe this is used instead
    is_available = models.BooleanField(default=True)  
    # Assigning a ForeignKey if each order is handled by one agent

    def __str__(self):
        return f"{self.full_name} - {self.vehicle_type}"



from django.db import models

class Place(models.Model):
    name = models.CharField(max_length=255)
    preferred_district = models.CharField(max_length=255)  # Instead of ForeignKey

    def __str__(self):
        return f"{self.name} ({self.preferred_district})"
    
    from django.db import models

class DeliveryAssignment(models.Model):
    
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name='delivery_assignments')
    delivery_agent = models.ForeignKey(DeliveryAgent, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the assignment was made
    status = models.CharField(max_length=50, default='Assigned')  # Status of the assignment
    is_notified = models.BooleanField(default=False) 
    def __str__(self):
        return f"Delivery Assignment: Order {self.order.id} to {self.delivery_agent.full_name}"

from django.db import models

class DeliveryOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Transit', 'In Transit'),
        ('Out of Delivery', 'Out of Delivery'),
        ('Failed/Returned', 'Failed/Returned'),
        ('Delivered', 'Delivered'),
        ('Canceled', 'Canceled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DeliveryOrder {self.id} - {self.status}"



from django.conf import settings

class CustomOrder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    product_name = models.CharField(max_length=255)

    DURABILITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    durability = models.CharField(max_length=10, choices=DURABILITY_CHOICES)

    FINISH_CHOICES = [
        ('Glossy', 'Glossy'),
        ('Matte', 'Matte'),
        ('Rustic', 'Rustic'),
        ('Polished', 'Polished'),
        ('Unfinished', 'Unfinished'),
    ]
    finish = models.CharField(max_length=15, choices=FINISH_CHOICES)

    RESISTANCE_CHOICES = [
        ('water_resistant', 'Water Resistant'),
        ('scratch_resistant', 'Scratch Resistant'),
    ]
    resistance = models.CharField(max_length=20, choices=RESISTANCE_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_name} - {self.user.username}"

from django.db import models

class Material(models.Model):
    designer = models.ForeignKey(User, on_delete=models.CASCADE)  # Designer who adds the material
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='materials/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    from django.db import models

class Furniture(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class FurnitureImage(models.Model):
    furniture = models.ForeignKey(Furniture, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='furniture_images/')



class CustomizationRequest(models.Model):
    # Customer Details
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)

    # Furniture Selection
    FURNITURE_CHOICES = [
        ('dining_table', 'Dining Table'),
        ('sofa', 'Sofa & Sectional'),
        ('bed', 'Bed Frame & Headboard'),
        ('office_desk', 'Office Desk'),
        ('bookshelf', 'Bookshelf'),
        ('wardrobe', 'Wardrobe'),
        ('tv_unit', 'TV Unit'),
        ('coffee_table', 'Coffee Table'),
        ('chair', 'Chair (Dining/Office)'),
        ('outdoor_bench', 'Outdoor Bench'),
    ]
    furniture_type = models.CharField(max_length=50, choices=FURNITURE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # ✅ Dining Table
    dining_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    dining_width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    dining_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # ✅ Sofa & Sectional
    sofa_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    sofa_depth = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    sofa_seat_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # ✅ Bed Frame & Headboard (Single, Queen, King)
    bed_single_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bed_single_width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    
    bed_queen_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bed_queen_width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    
    bed_king_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bed_king_width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # ✅ Office Desk
    desk_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    desk_width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    desk_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # ✅ Bookshelf
    bookshelf_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bookshelf_width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bookshelf_depth = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # ✅ Wardrobe
    wardrobe_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    wardrobe_width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    wardrobe_depth = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # ✅ TV Unit
    tv_unit_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tv_unit_depth = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    tv_unit_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # ✅ Coffee Table
    coffee_table_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    coffee_table_width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    coffee_table_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # ✅ Chair (Dining/Office)
    chair_seat_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    chair_width = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    chair_depth = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # ✅ Outdoor Bench
    bench_length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bench_depth = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    bench_seat_height = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    # Material & Wood Type (Dropdown from DB)
    material = models.ForeignKey(Material, on_delete=models.SET_NULL, null=True, blank=True)
    wood_type = models.ForeignKey(Furniture, on_delete=models.SET_NULL, null=True, blank=True)

    # Color & Finish
    color = models.CharField(max_length=50, blank=True, null=True)
    finish = models.CharField(max_length=50, choices=[('matte', 'Matte'), ('glossy', 'Glossy')], blank=True, null=True)

    # Additional Features
    storage_options = models.TextField(blank=True, null=True)  # Drawers, shelves, etc.
    special_features = models.TextField(blank=True, null=True)  # Carvings, special design elements

    # Image Uploads (Design Inspiration / Sketch / 3D Model)
    reference_image = models.ImageField(upload_to='customization_images/', blank=True, null=True)
    sketch_or_3d_model = models.FileField(upload_to='designs/', blank=True, null=True)

    # Delivery Options
    expected_delivery_date = models.DateField(blank=True, null=True)
    urgent_request = models.BooleanField(default=False)

    # Request Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.furniture_type} ({self.status})"
    
    
from django.db import models
class Payment(models.Model):
    customization_request = models.ForeignKey('CustomizationRequest', on_delete=models.CASCADE)
    price_furniture = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_material = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_wood = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_color = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_storage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_features = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_finish = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_urgent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_price_finalized = models.BooleanField(default=False)  # NEW FIELD

    def calculate_total(self):
        return sum(filter(None, [
            self.price_furniture,
            self.price_material,
            self.price_wood,
            self.price_color,
            self.price_storage,
            self.price_features,
            self.price_finish,
            self.price_urgent
        ]))

    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total()
        super().save(*args, **kwargs)
        if hasattr(self, 'customization_request'):
            self.customization_request.total_price = self.total_price
            self.customization_request.save()

    def __str__(self):
        return f"Payment for {self.customization_request.full_name}"
