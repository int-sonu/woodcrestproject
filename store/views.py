from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.views.decorators.cache import cache_control
from store.models import User, Orders, DeliveryAgent, DeliveryAssignment

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')  # Redirect to home if already logged in

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            if user.status == 'blocked':
                return redirect('blocked')  # Redirect to account blocked page

            # Log the user in
            auth_login(request, user)

            # If the user is a delivery agent, check profile completion
            if user.is_delivery_agent():
                if not hasattr(user, 'deliveryagent') or not user.deliveryagent.profile_completed:
                    return redirect('complete_profile')  # Only delivery agents must complete profile

            # Redirect based on user role
            if user.is_admin():
                return redirect('admin_dashboard')
            elif user.is_seller():
                return redirect('seller_dashboard')
            elif user.is_delivery_agent():
                return redirect('delivery_dashboard')
            elif user.is_designer():
                return redirect('designer_dashboard')
            else:
                return redirect('index')  # Redirect to home for regular users
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

    return render(request, 'register.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')
        password = request.POST.get('password')
        role = request.POST.get('role', 'user')  # Default to 'user' if no role is selected

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            try:
                user = User(
                    username=username,
                    email=email,
                    mobile_number=mobile_number,
                    pincode=pincode,
                    address=address,
                    role=role,
                    is_approved=False if role in ['seller', 'delivery_agent', 'designer'] else True
                )
                user.set_password(password)  # Hash the password
                user.save()
                
                if role == 'seller':
                    messages.success(request, 'Registration successful. Your account is pending approval.')
                elif role == 'delivery_agent':
                    messages.success(request, 'Registration successful. Your account is pending approval as a delivery agent.')
                elif role == 'designer':
                    messages.success(request, 'Registration successful. Your account is pending approval as a designer.')
                else:
                    messages.success(request, 'Registration successful.')
                    
                return redirect('login')
            except IntegrityError:
                messages.error(request, 'An error occurred while creating the user.')

    return render(request, 'register.html')




from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def designer_dashboard(request):
    return render(request, 'designer/designer_dashboard.html')  # Ensure this template exists




from django.shortcuts import render

def blocked_view(request):
    return render(request, 'blocked.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User

@login_required
def admin_dashboard(request):
    if not request.user.is_admin:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('index')  # Redirect to home if not an admin

    # Calculate totals
    total_users = User.objects.filter(is_superuser=False).count()  # Count regular users
    total_categories = Category.objects.count()  # Count total categories
    total_subcategories = SubCategory.objects.count()  # Count total subcategories
    total_products = Product.objects.count()  # Count total products
    total_orders = Orders.objects.count()  # Assuming you have an Orders model
    total_customizations = 0  # Replace with actual logic if you have a Customization model
    total_feedback = 0  # Replace with actual logic if you have a Feedback model

    context = {
        'total_users': total_users,
        'total_categories': total_categories,
        'total_subcategories': total_subcategories,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_customizations': total_customizations,
        'total_feedback': total_feedback,
    }

    return render(request, 'admin/admin_dashboard.html', context)  # Render admin dashboard template

@login_required
def seller_dashboard(request):
    if not request.user.is_seller:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('index')  # Redirect to home if not a seller
    return render(request, 'seller/seller_dashboard.html')  # Render seller dashboard template


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def delivery_dashboard(request):
    return render(request, "delivery_agent/delivery_dashboard.html")


def complete_profile_view(request):
    user = request.user

    try:
        delivery_agent = DeliveryAgent.objects.get(user=user)
        
        # Check if all required fields are filled and profile is complete
        if (
            delivery_agent.full_name and
            delivery_agent.email and
            delivery_agent.phone_number and
            delivery_agent.vehicle_type and
            delivery_agent.vehicle_id and
            delivery_agent.delivery_area and
            delivery_agent.address and
            delivery_agent.gender and
            delivery_agent.emergency_contact and
            delivery_agent.bank_details
        ):
            if delivery_agent.is_approved:
                messages.info(request, "Your profile is already complete and approved.")
                return redirect('delivery_dashboard')  # Redirect to dashboard if approved
            else:
                messages.info(request, "Your profile is complete, awaiting approval.")
                return redirect('login')  # Redirect to login if awaiting approval
    
    except DeliveryAgent.DoesNotExist:
        delivery_agent = None  

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        vehicle_type = request.POST.get('vehicle_type')
        vehicle_id = request.POST.get('vehicle_id')
        delivery_area = request.POST.get('delivery_area')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        emergency_contact = request.POST.get('emergency_contact')
        bank_details = request.POST.get('bank_details')

        if delivery_agent:
            # Update existing profile
            delivery_agent.full_name = full_name
            delivery_agent.email = email
            delivery_agent.phone_number = phone_number
            delivery_agent.vehicle_type = vehicle_type
            delivery_agent.vehicle_id = vehicle_id
            delivery_agent.delivery_area = delivery_area
            delivery_agent.address = address
            delivery_agent.gender = gender
            delivery_agent.emergency_contact = emergency_contact
            delivery_agent.bank_details = bank_details
            delivery_agent.save()
        else:
            # Create new profile
            DeliveryAgent.objects.create(
                user=user,
                full_name=full_name,
                email=email,
                phone_number=phone_number,
                vehicle_type=vehicle_type,
                vehicle_id=vehicle_id,
                delivery_area=delivery_area,
                address=address,
                gender=gender,
                emergency_contact=emergency_contact,
                bank_details=bank_details
            )

        messages.success(request, "Profile submitted successfully for approval.")
        return redirect('login')  # Redirect to login after submission for approval

    return render(request, "delivery_agent/complete_profile.html", {"delivery_agent": delivery_agent})





# Assuming you have a home page view
@login_required
def index(request):
    return render(request, 'index.html')  # Render home page template

from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib import messages

User = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('password_reset_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
            })
            send_mail(mail_subject, message, 'admin@yourdomain.com', [email])
            messages.success(request, 'Password reset email has been sent.')
        except User.DoesNotExist:
            messages.error(request, 'Email does not exist.')
    return render(request, 'forgot_password.html')

def reset_password(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            user.set_password(password)
            user.save()
            messages.success(request, 'Password has been reset.')
            return redirect('login')
        return render(request, 'reset_password.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.error(request, 'Password reset link is invalid.')
        return redirect('forgot_password')
    
    
    
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def logout_view(request):
    auth_logout(request)
    request.session.flush()  
    return redirect('login')  



#update profile
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        pincode = request.POST.get('pincode')
        address = request.POST.get('address')

        # Update user information
        user.username = username
        user.email = email
        user.mobile_number = mobile_number
        user.pincode = pincode
        user.address = address
        
        # Save user information
        user.save()
        
        # Add a success message
        messages.success(request, 'Your information has been updated successfully.')
        
        return redirect('index')  # Redirect to the index or any other preferred page
    
    # Render the profile update form
    return render(request, 'update_profile.html', {'user': request.user})



def view_customers(request):
    customers = User.objects.filter(is_superuser=False)  
    context = {
        'customers': customers
    }
    return render(request, 'admin/view_customers.html', context)

def toggle_status(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if category.status == 'Active':
        category.status = 'Inactive'
    else:
        category.status = 'Active'
    category.save()
    return redirect('view_category')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        status = request.POST.get('status', 'active')  # Default to 'active' if not provided
        
        # Check if the name is provided
        if not name:
            messages.error(request, 'Category name is required.')
            return render(request, 'admin/add_category.html', {'error': 'This field is required.'})

        # Check if the category already exists
        if Category.objects.filter(name=name).exists():
            messages.error(request, 'A category with this name already exists.')
            return render(request, 'admin/add_category.html', {'error': 'A category with this name already exists.'})

        # Check if the name starts with a capital letter
        if not name[0].isupper():
            messages.error(request, 'The category name must start with a capital letter.')
            return render(request, 'admin/add_category.html', {'error': 'The category name must start with a capital letter.'})

        # Check if the name contains numbers
        if any(char.isdigit() for char in name):
            messages.error(request, 'The category name should not contain numbers.')
            return render(request, 'admin/add_category.html', {'error': 'The category name should not contain numbers.'})

        # Create the category if all checks pass
        Category.objects.create(name=name, status=status)
        messages.success(request, 'Category created successfully.')
        return redirect('view_category')
    
    return render(request, 'admin/add_category.html')



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category

def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')

        # Validation
        if not name:
            messages.error(request, 'Category name is required.')
            return render(request, 'admin/edit_category.html', {'category': category, 'error': 'This field is required.'})

        if not name[0].isupper():
            messages.error(request, 'The category name must start with a capital letter.')
            return render(request, 'admin/edit_category.html', {'category': category, 'error': 'The category name must start with a capital letter.'})

        if any(char.isdigit() for char in name):
            messages.error(request, 'The category name should not contain numbers.')
            return render(request, 'admin/edit_category.html', {'category': category, 'error': 'The category name should not contain numbers.'})

        # Update category
        category.name = name
        category.save()
        messages.success(request, 'Category updated successfully.')
        return redirect('view_category')

    return render(request, 'admin/edit_category.html', {'category': category})


# View to delete a category
def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('view_category')
    return render(request, 'admin/delete_category.html', {'category': category})


#def index(request):
    ##categories = Category.objects.prefetch_related('subcategories').all()
    #products = Product.objects.all()
    #return render(request, 'index.html', {'categories': categories, 'products': products})#

# View to list all categories
def view_category(request):
    categories = Category.objects.all()
    return render(request, 'admin/view_category.html', {'categories': categories})


def view_subcategories(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'admin/view_subcategories.html', {'subcategories': subcategories})


from django.shortcuts import render
from .models import Category, SubCategory

# View for sellers to view all categories
def seller_view_categories(request):
    categories = Category.objects.all()
    return render(request, 'seller/categories.html', {'categories': categories})

# View for sellers to view all subcategories
def seller_view_subcategories(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'seller/subcategories.html', {'subcategories': subcategories})


import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Category, SubCategory

def add_subcategory(request):
    if request.method == 'POST':
        category_id = request.POST.get('category')
        sub_name = request.POST.get('sub_name')

        # Validation checks
        if not sub_name:
            return render(request, 'admin/add_subcategory.html', {'error': 'This field is required.', 'categories': Category.objects.all()})

        if not sub_name[0].isupper():
            return render(request, 'admin/add_subcategory.html', {'error': 'The subcategory name must start with a capital letter.', 'categories': Category.objects.all()})

        if any(char.isdigit() for char in sub_name):
            return render(request, 'admin/add_subcategory.html', {'error': 'The subcategory name should not contain numbers.', 'categories': Category.objects.all()})

        if re.search(r'[^a-zA-Z\s]', sub_name):
            return render(request, 'admin/add_subcategory.html', {'error': 'Subcategory name must not contain symbols.', 'categories': Category.objects.all()})

        category = Category.objects.get(id=category_id)
        if SubCategory.objects.filter(category=category, sub_name=sub_name).exists():
            return render(request, 'admin/add_subcategory.html', {'error': 'This subcategory already exists in the selected category.', 'categories': Category.objects.all()})

        SubCategory.objects.create(category=category, sub_name=sub_name)
        return redirect('view_subcategories')  # Replace with your desired redirect URL

    categories = Category.objects.all()
    return render(request, 'admin/add_subcategory.html', {'categories': categories})


from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Category

def edit_subcategory(request, id):
    subcategory = get_object_or_404(SubCategory, id=id)
    categories = Category.objects.all()

    if request.method == 'POST':
        sub_name = request.POST.get('sub_name')
        category_id = request.POST.get('category')
        status = request.POST.get('status', True)  # Default to True if not provided

        if not sub_name:
            messages.error(request, 'Subcategory name is required.')
            return render(request, 'admin/edit_subcategory.html', {'subcategory': subcategory, 'categories': categories})

        if not sub_name[0].isupper():
            messages.error(request, 'The subcategory name must start with a capital letter.')
            return render(request, 'admin/edit_subcategory.html', {'subcategory': subcategory, 'categories': categories})

        if any(char.isdigit() for char in sub_name):
            messages.error(request, 'The subcategory name should not contain numbers.')
            return render(request, 'admin/edit_subcategory.html', {'subcategory': subcategory, 'categories': categories})

        if re.search(r'[^a-zA-Z\s]', sub_name):
            messages.error(request, 'Subcategory name must not contain symbols.')
            return render(request, 'admin/edit_subcategory.html', {'subcategory': subcategory, 'categories': categories})

        category = Category.objects.get(id=category_id)

        subcategory.sub_name = sub_name
        subcategory.category = category
        subcategory.status = status
        subcategory.save()

        messages.success(request, 'SubCategory updated successfully.')
        return redirect('view_subcategories')

    return render(request, 'admin/edit_subcategory.html', {'subcategory': subcategory, 'categories': categories})


def delete_subcategory(request, id):
    subcategory = get_object_or_404(SubCategory, id=id)
    subcategory.delete()
    return redirect('view_subcategories')

from django.shortcuts import render
from .models import Category, SubCategory

def view_subcategories(request):
    subcategories = SubCategory.objects.all()
    return render(request, 'admin/view_subcategories.html', {'subcategories': subcategories})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import User  # Adjust the import based on your actual model location


def toggle_subcategory_status(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    subcategory.status = not subcategory.status
    subcategory.save()
    return redirect('view_subcategories') 

from django.shortcuts import get_object_or_404, redirect
from .models import User

def toggle_customer_status(request, user_id):
    customer = get_object_or_404(User, pk=user_id)
    if customer.status == 'active':
        customer.status = 'blocked'
    else:
        customer.status = 'active'
    customer.save()
    return redirect('view_customers')

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Category, SubCategory, Product, Image
import re
from django.shortcuts import render, redirect
from .models import Product, Category, SubCategory, Seat
from django.shortcuts import render, redirect
from .models import Product, Seat, Category, SubCategory
from django.shortcuts import render, redirect
from .models import Product, Category, SubCategory, Seat, Image

from decimal import Decimal, InvalidOperation  # Add this import

def add_product_view(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        category_id = request.POST.get('category')
        subcategory_id = request.POST.get('subcategory')
        wood = request.POST.get('wood')
        price = request.POST.get('price')
        color = request.POST.get('color')
        stock = request.POST.get('stock')
        description = request.POST.get('description')
        additional_info = request.POST.get('additional_info')

        # Validate Price
        try:
            price = Decimal(price)  # Attempt to convert price to a Decimal
        except (ValueError, InvalidOperation):
            raise ValidationError('Price must be a valid decimal number.')

        # Validate Stock
        try:
            stock = int(stock)  # Ensure stock is an integer
        except ValueError:
            raise ValidationError('Stock must be a valid integer.')

        # Create Product instance
        category = Category.objects.get(id=category_id)
        subcategory = SubCategory.objects.get(id=subcategory_id)

        # Fetch the SellerProfile instance for the current user
        try:
            seller_profile = SellerProfile.objects.get(user=request.user)
        except SellerProfile.DoesNotExist:
            return HttpResponse("Seller profile not found", status=404)

        product = Product.objects.create(
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            wood=wood,
            price=price,
            color=color,
            stock=stock,
            description=description,
            additional_info=additional_info,
            seller=seller_profile  # Correctly assign the instance
        )

        # Handle Image Uploads
        images = request.FILES.getlist('images')
        for image in images:
            Image.objects.create(
                product=product,
                image=image
            )

        return redirect('view_product')

    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()

    return render(request, 'seller/add_product.html', {'categories': categories, 'subcategories': subcategories})

def view_product(request):
    products = Product.objects.all()
    return render(request, 'seller/view_product.html', {'products': products})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all()
    subcategories = SubCategory.objects.all()
    
    if request.method == 'POST':
        product_name = request.POST['product_name']
        category_id = request.POST['category']
        subcategory_id = request.POST['subcategory']
        wood = request.POST['wood']
        price = request.POST['price']
        color = request.POST['color']
        stock_to_add = int(request.POST['stock'])
        description = request.POST['description']

        # Update product details
        product.product_name = product_name
        product.category_id = category_id
        product.subcategory_id = subcategory_id
        product.wood = wood
        product.price = price
        product.color = color
        product.stock += stock_to_add  # Add new stock to the existing stock
        product.description = description

        if 'image' in request.FILES:
            product.image = request.FILES['image']

        product.save()
        return redirect('view_product')

    return render(request, 'seller/edit_product.html', {
        'product': product,
        'categories': categories,
        'subcategories': subcategories,
    })


def delete_product(request, product_id):
    subcategory = get_object_or_404(Product, id=product_id)
    subcategory.delete()
    return redirect('view_product')

from django.shortcuts import render
from .models import Category, SubCategory, Product  # Import your models

def seller_dashboard_view(request):
    # Fetch data
    total_categories = Category.objects.count()
    total_subcategories = SubCategory.objects.count()
    total_products = Product.objects.count()

    # Prepare context
    context = {
        'total_categories': total_categories,
        'total_subcategories': total_subcategories,
        'total_products': total_products,
    }

    # Render the template with the context
    return render(request, 'seller/seller_dashboard.html', context)



# views.py
from django.shortcuts import render
from .models import Product

def search_products(request):
    query = request.GET.get('s')  
    if query:
        products = Product.objects.filter(product_name__icontains=query)  
    else:
        products = Product.objects.all() 

    context = {
        'products': products,
        'query': query,  
    }
    return render(request, 'search_results.html', context)


def category_display(request, category_name):
    # Fetch the category based on the name
    category = get_object_or_404(Category, name=category_name)

    # Fetch products under this category
    products = Product.objects.filter(category=category)

    return render(request, 'category_display.html', {'category': category, 'products': products})

from django.shortcuts import render, get_object_or_404
from .models import SubCategory

def subcategory_detail(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, id=subcategory_id)
    products = subcategory.products.all()
    categories = Category.objects.prefetch_related('subcategories').all()  # Fetch categories with subcategories
    
    context = {
        'subcategory': subcategory,
        'products': products,
        'categories': categories,  # Pass categories to the template
    }
    return render(request, 'subcategory_detail.html', context)



from django.shortcuts import render

def blocked_view(request):
    return render(request, 'blocked.html')

from django.shortcuts import render, get_object_or_404
from .models import Product

# views.py
from django.shortcuts import render, get_object_or_404
from .models import Product, Seat

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    seats = product.seats.all() 
    categories = Category.objects.prefetch_related('subcategories').all()  # Fetch categories with subcategories
    
    return render(request, 'product_detail.html', {
        'product': product,
        'seats': seats,
        'categories': categories,  # Pass categories to the template
    })

#user can view the page

def index(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    products = Product.objects.all()
    return render(request, 'index.html', {'categories': categories, 'products': products})

# views.py
from django.shortcuts import render
from .models import SellerProfile  # Import the SellerProfile model

def view_sellers(request):
    sellers = SellerProfile.objects.all()  # Fetch all seller profiles
    context = {
        'sellers': sellers
    }
    return render(request, 'admin/view_sellers.html', context)

from django.shortcuts import render
from .models import Product

def view_seller_products(request):
    products = Product.objects.all()
    return render(request, 'admin/views_product.html', {'products': products})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Cart

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user = request.user
    
    # Get the quantity from the request, default to 1 if not provided
    quantity = int(request.GET.get('quantity', 1))
    
    # Get or create the cart item
    cart_item, created = Cart.objects.get_or_create(
        user=user, 
        product=product, 
        status='Pending',
        defaults={'amount': product.price * quantity, 'quantity': quantity}  # Corrected defaults
    )
    
    if not created:
        # Update the existing cart item: Set quantity to the new quantity from the request
        cart_item.quantity = quantity  # Update quantity to the new one
        cart_item.amount = cart_item.quantity * product.price  # Recalculate the total amount
        cart_item.save()
    
    return redirect('view_cart')  # Redirect to the cart view


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cart

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user, status='Pending')
  
    for item in cart_items:
        item.total_price = item.quantity * item.product.price
  
    total = sum(item.total_price for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})



from django.shortcuts import redirect, get_object_or_404
from .models import Cart

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=item_id)
        cart_item.delete()
        return redirect('view_cart')  
    else:
        return redirect('view_cart')
    

from django.shortcuts import render, redirect
from .models import User, Cart
def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user = request.user  
    cart_items = Cart.objects.filter(user=user)  
    grand_total = sum(item.total_cost() for item in cart_items)  

    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        amount = grand_total  # Use the grand total for the payment amount

        # Create the payment record
        try:
            payment = Payment(
                user=user,
                amount=Decimal(amount),
                payment_method=payment_method
            )
            payment.full_clean()
            payment.save()

            # Create the order record
            order = Order(
                user=user,
                payment=payment,  # Link to the payment record
                order_total=Decimal(amount)
            )
            order.full_clean()
            order.save()

            cart_items.delete()  # Clear the cart after successful payment

            return redirect('confirmation_view')

        except (ValueError, ValidationError) as e:
            print(f"Error processing payment or order: {e}")

    context = {
        'user': user,
        'cart_items': cart_items,
        'grand_total': grand_total
    }

    return render(request, 'checkout.html', context)




def process_checkout(request):
    if request.method == 'POST':
       
        return redirect('success_page') 
    else:
        return redirect('checkout') 


from django.shortcuts import render, redirect
from .models import SellerProfile

def seller_profile(request):
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pincode = request.POST.get('pincode')
        password = request.POST.get('password')
        business_name = request.POST.get('business_name')
        gst_number = request.POST.get('gst_number')
        business_pan_card = request.POST.get('business_pan_card')
        cheque_passbook_photo = request.FILES.get('cheque_passbook_photo')
        sign = request.FILES.get('sign')
        account_holder_name = request.POST.get('account_holder_name')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')

        # Create and save the SellerProfile instance
        SellerProfile.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address,
            city=city,
            pincode=pincode,
            password=password,
            business_name=business_name,
            gst_number=gst_number,
            business_pan_card=business_pan_card,
            cheque_passbook_photo=cheque_passbook_photo,
            sign=sign,
            account_holder_name=account_holder_name,
            account_number=account_number,
            ifsc_code=ifsc_code,
        )
        return redirect('seller_dashboard')  # Replace 'success_url' with your actual URL
    return render(request, 'seller/seller_profile.html')

from django.shortcuts import render, get_object_or_404
from .models import SellerProfile

def view_seller(request, seller_id):
    seller_profile = get_object_or_404(SellerProfile, id=seller_id)
    return render(request, 'seller/view_seller.html', {'seller_profile': seller_profile})
# store/views.py
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import SellerProfile

@login_required
def approve_seller(request, seller_id):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admin users

    seller = get_object_or_404(SellerProfile, id=seller_id)
    seller.is_approved = True
    seller.is_pending = False
    seller.is_rejected = False
    seller.save()
    
    # Send approval email
    subject = 'Your Seller Account Has Been Approved'
    message = f"Dear {seller.name},\n\nYour seller account has been approved. You can now start listing your products.\n\nBest regards,\n {seller.business_name}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [seller.email]

    send_mail(subject, message, from_email, recipient_list)

    return redirect('view_sellers')  # Redirect to the seller list or any other page

@login_required
def pending_seller(request, seller_id):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admin users

    seller = get_object_or_404(SellerProfile, id=seller_id)
    seller.is_approved = False
    seller.is_pending = True
    seller.is_rejected = False
    seller.save()
    
    # Send pending email
    subject = 'Your Seller Account Status Update'
    message = f"Dear {seller.name},\n\nYour seller account is now in pending status. We will review your application soon.\n\nBest regards,\n{seller.business_name}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [seller.email]

    send_mail(subject, message, from_email, recipient_list)

    return redirect('view_sellers')  # Redirect to the seller list or any other page

@login_required
def reject_seller(request, seller_id):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admin users

    seller = get_object_or_404(SellerProfile, id=seller_id)
    seller.is_approved = False
    seller.is_pending = False
    seller.is_rejected = True
    seller.save()
    
    # Send rejection email
    subject = 'Your Seller Account Has Been Rejected'
    message = f"Dear {seller.name},\n\nWe regret to inform you that your seller account has been rejected. If you have any questions or need further information, please contact us.\n\nBest regards,\n {seller.business_name}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [seller.email]

    send_mail(subject, message, from_email, recipient_list)

    return redirect('view_sellers')  # Redirect to the seller list or any other page

@login_required
def reject_seller(request, seller_id):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admin users

    seller = get_object_or_404(SellerProfile, id=seller_id)
    seller.is_approved = False
    seller.is_pending = False
    seller.is_rejected = True
    seller.save()
    
    # Send rejection email
    subject = 'Your Seller Account Has Been Rejected'
    message = f"Dear {seller.name},\n\nUnfortunately, your seller account has been rejected. Please contact support for further details.\n\nBest regards,\n {seller.business_name}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [seller.email]

    send_mail(subject, message, from_email, recipient_list)

    return redirect('view_sellers')  # Redirect to the seller list or any other page

@login_required
def mark_seller_pending(request, seller_id):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admin users

    seller = get_object_or_404(SellerProfile, id=seller_id)
    seller.is_approved = False
    seller.is_pending = True
    seller.is_rejected = False
    seller.save()
    
    # Send pending email
    subject = 'Your Seller Account is Pending Approval'
    message = f"Dear {seller.name},\n\nYour seller account is currently pending approval. We will notify you once the review is complete.\n\nBest regards,\n {seller.business_name}"
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [seller.email]

    send_mail(subject, message, from_email, recipient_list)

    return redirect('view_sellers')  # Redirect to the seller list or any other page

from django.shortcuts import get_object_or_404, redirect
from .models import SellerProfile  # Ensure you import the correct model

def pending_seller(request, seller_id):
    if not request.user.is_superuser:
        return redirect('home')  # Redirect non-admin users

    seller = get_object_or_404(SellerProfile, id=seller_id)  # Use the correct model name
    seller.status = 'Pending'
    seller.save()
    
    return redirect('view_sellers')


def custom_view(request):
    # Assuming you want to display custom categories on the index page
    return render(request, 'custom.html')

# views.py
from django.shortcuts import render

def custom_page_view(request):
    return render(request, 'custom.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomRequest
from django.contrib.auth.decorators import login_required

@login_required
def create_custom_request(request):
    if request.method == "POST":
        # Create and save the CustomRequest object
        custom_request = CustomRequest(
            user=request.user,  # Set the user field to the currently logged-in user
            city=request.POST.get('city'),
            custom_requirements=request.POST.get('custom_requirements'),
            image=request.FILES.get('image')  # Handle file upload
        )
        custom_request.save()

        messages.success(request, "Your custom request has been submitted successfully!")
        return redirect('custom')  # Redirect to a success page or any other page

    return render(request, 'create_custom_request.html')


def create_custom_requests(request):
    # Assuming you want to display custom categories on the index page
    custom_categories = CustomCategory.objects.all()
    return render(request, 'create_custom_request.html', {'custom_categories': custom_categories})

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import CustomRequest

@login_required
def seller_page(request):
    # Fetch all custom requests (or filter by specific criteria if needed)
    custom_requests = CustomRequest.objects.all()  # Adjust the queryset as needed
    return render(request, 'seller/seller_page.html', {'custom_requests': custom_requests})

from django.shortcuts import render
from .models import Category

def category_view(request):
     categories = Category.objects.prefetch_related('subcategories').all()
     return render(request, 'subcategory_detail.html', {'categories': categories})

from django.shortcuts import render
from .models import Product

def product_list(request):
    # Get selected wood types from request
    wood_types = request.GET.getlist('wood_type')

    # Start with all products
    products = Product.objects.all()

    # Apply wood type filter if any wood types are selected
    if wood_types:
        products = products.filter(wood__in=wood_types)
    
    # Optionally, apply other filters (e.g., price, seats) here
    
    # Pass the filtered products to the template
    context = {
        'products': products,
    }
    return render(request, 'subcategory_detail.html', context)

from django.shortcuts import render
from .models import Product

def product_list_view(request):
    sort_by = request.GET.get('sort_by', 'name')  # Default sorting by 'name'

    if sort_by == 'price_low_to_high':
        products = Product.objects.all().order_by('price')
    elif sort_by == 'price_high_to_low':
        products = Product.objects.all().order_by('-price')
    elif sort_by == 'newest_first':
        products = Product.objects.all().order_by('-created_at')  # Adjust field as needed
    elif sort_by == 'best_selling':
        products = Product.objects.all().order_by('-sales')  # Assuming you have a 'sales' field
    else:
        products = Product.objects.all()  # Default sorting

    return render(request, 'subcategory_detail.html', {'products': products})

# views.py
from django.shortcuts import render
from .models import Comment

def submit_comment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        rating = request.POST.get('rating')
        comment_text = request.POST.get('comment')
        
        # Save the comment
        Comment.objects.create(name=name, email=email, rating=rating, comment=comment_text)
        
        return redirect('user_page')  # Redirect to the user page after saving

    return render(request, 'comment_form.html')  # Render the form if not POST


# views.py
from django.shortcuts import render
from .models import Comment, SellerProfile  # Import your Seller model if needed

def seller_comments(request):
    comments = Comment.objects.all()  # Fetch all comments
    # Add any other seller-related data here
    return render(request, 'seller/seller_comments.html', {'comments': comments})


def admin_comments(request):
    comments = Comment.objects.all()  # Fetch all comments
    # Add any other admin-related data here
    return render(request, 'admin/admin_comments.html', {'comments': comments})

from .models import Comment, Category, SubCategory, Product  # Ensure Product model is imported

def index(request):
    comments = Comment.objects.all()  # Fetch all comments
    stars = range(5)  # Pass a range from 0 to 4 (5 total stars)
    categories = Category.objects.all()  # Fetch all categories
    subcategories = SubCategory.objects.all()  # Fetch all subcategories
    products = Product.objects.all()  # Fetch all products

    context = {
        'comments': comments,
        'stars': stars,
        'categories': categories,
        'subcategories': subcategories,
        'products': products,  # Add products to context
    }
    return render(request, 'index.html', context)

from django.shortcuts import render

def thank_you_view(request):
    return render(request, 'thank-you.html')





from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Orders, Cart
import razorpay
from django.conf import settings
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET))

@login_required
def place_order(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        user = request.user

        # Get the user's cart items
        cart_items = Cart.objects.filter(user=user)

        # Check if the cart is empty
        if not cart_items.exists():
            return render(request, 'checkout.html', {'error': 'Your cart is empty. Please add items to your cart before placing an order.'})

        # Create orders for each cart item
        orders = []
        for item in cart_items:
            order = Orders.objects.create(
                user=user,
                product=item.product,
                quantity=item.quantity,  # Save the quantity from the cart
                amount=item.total_cost(),
                payment_method=payment_method,
                created_at=timezone.now()
            )
            orders.append(order)

        # Clear the cart after the order is placed
        cart_items.delete()

        if payment_method == "cash_on_delivery":
            # Update payment status for cash on delivery
            for order in orders:
                order.payment_status = 'Paid'  # Assuming payment is confirmed for COD
                order.save()

            # Redirect to order confirmation page for Cash on Delivery
            return render(request, 'order_success.html', {'orders': orders})

        elif payment_method == "online_payment":
            # Calculate total amount for Razorpay
            total_amount = int(sum(order.amount for order in orders) * 100)  # Razorpay expects amount in paise

            # Create Razorpay order
            razorpay_order = razorpay_client.order.create({
                "amount": total_amount,
                "currency": "INR",
                "payment_capture": "1"  # Automatic capture
            })

            # Pass the Razorpay order ID and amount to the payment page
            context = {
                'orders': orders,
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_key': settings.RAZORPAY_KEY_ID,
                'total_amount': total_amount,
            }
            return render(request, 'razorpay_payment.html', context)

    # If it's a GET request, render the checkout page with cart summary
    cart_items = Cart.objects.filter(user=request.user)
    grand_total = sum(item.total_cost() for item in cart_items)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'grand_total': grand_total})


import hashlib
import hmac
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .models import Orders

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET))

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        try:
            # Extract Razorpay payment details from the POST request
            razorpay_payment_id = request.POST.get('razorpay_payment_id')
            razorpay_order_id = request.POST.get('razorpay_order_id')
            razorpay_signature = request.POST.get('razorpay_signature')

            # Ensure required fields are present
            if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
                return render(request, 'order_failure.html', {'error': 'Missing payment details'})

            # Verify the Razorpay signature
            generated_signature = hmac.new(
                settings.RAZORPAY_SECRET.encode(),
                f"{razorpay_order_id}|{razorpay_payment_id}".encode(),
                hashlib.sha256
            ).hexdigest()

            if generated_signature != razorpay_signature:
                return render(request, 'order_failure.html', {'error': 'Payment verification failed'})

            # Retrieve the orders associated with this Razorpay order ID
            orders = Orders.objects.filter(payment_method='Razorpay', payment_status='Pending', razorpay_order_id=razorpay_order_id)

            if not orders.exists():
                return render(request, 'payment_success.html', {'error': 'No pending orders found for this payment'})

            # Update the status of all orders linked to this Razorpay order
            for order in orders:
                order.payment_status = 'Paid'
                order.razorpay_payment_id = razorpay_payment_id
                order.save()

            # You can log or process each order quantity here, if needed
            total_quantity = sum(order.quantity for order in orders)

            # Redirect to the order success page after successful payment
            return render(request, 'payment_success.html', {'orders': orders, 'total_quantity': total_quantity})

        except Exception as e:
            return render(request, 'order_failure.html', {'error': str(e)})

    return render(request, 'order_failure.html', {'error': 'Invalid request method'})





from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Orders  # Ensure your Orders model is imported

@login_required
def view_order(request, order_id):
    # Fetch the order for the logged-in user
    order = get_object_or_404(Orders, id=order_id, user=request.user)

    return render(request, 'order_success.html', {'order': order})



# store/views.py
from django.shortcuts import redirect, get_object_or_404
from .models import Wishlist, Product

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not created:
        # If the item already exists, remove it from the wishlist
        wishlist_item.delete()
        return redirect('product_detail', pk=product_id)  # Redirect back to the product detail page

    return redirect('product_detail', pk=product_id)  # Redirect back to the product detail page

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from .models import Product, Wishlist
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import Product, Wishlist

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is already in the user's wishlist
    if not Wishlist.objects.filter(user=request.user, product=product).exists():
        # Logic to add the product to the wishlist
        Wishlist.objects.create(user=request.user, product=product)
    
    # You can also add a message if you want to notify the user
    # messages.success(request, f'{product.name} has been added to your wishlist.')

    return redirect('product_detail', pk=product_id)  # Correct argument here


from django.urls import path
from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist, Product  # Adjust based on your actual models
from django.contrib.auth.decorators import login_required

@login_required
def wishlist_view(request):
    # Get the current user's wishlist items
    wishlist_items = Wishlist.objects.filter(user=request.user)  # Adjust as needed
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})
@login_required
def remove_from_wishlist(request, product_id):
    if request.method == 'POST':
        # Remove the product from the user's wishlist
        wishlist_items = Wishlist.objects.filter(user=request.user, product_id=product_id)

        if wishlist_items.exists():
            wishlist_items.delete()  # Delete all instances of the wishlist item
        return redirect('wishlist')  # Redirect to the wishlist page after removal


from django.shortcuts import render, get_object_or_404
from .models import Orders  # Ensure your Orders model is imported

def view_orders(request):
    orders = Orders.objects.filter(user=request.user)  # Fetch orders for the logged-in user
    return render(request, 'view_orders.html', {'orders': orders})

def order_details(request, order_id):
    order = get_object_or_404(Orders, id=order_id, user=request.user)  # Fetch the order for the logged-in user
    return render(request, 'order_details.html', {'order': order})

from django.shortcuts import render
from store.models import Orders

def my_orders(request):
    orders = Orders.objects.filter(user=request.user)  # Adjust your query as necessary
    
    # Check for a search query
    query = request.GET.get('query')
    if query:
        # Filter orders by product name ignoring case
        orders = orders.filter(product__product_name__icontains=query)

    return render(request, 'view_orders.html', {'orders': orders})


def remove_order(request, order_id):
    # Get the order object
    order = get_object_or_404(Orders, id=order_id, user=request.user)
    
    # Delete the order
    order.delete()
    
    # Redirect to the orders page
    return redirect('my_orders') 

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Orders, Contact  # Adjust the import based on your models

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Save contact message in the database
        Contact.objects.create(name=name, email=email, message=message)
        return redirect('index')  # Redirect to the orders page

    return render(request, 'contact.html')

def submit_rating(request, order_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        rating = data['rating']
        # Save the rating to the database
        order = Order.objects.get(id=order_id)
        order.rating = rating  # Assuming you have a field for rating in your Order model
        order.save()
        return JsonResponse({'success': True})

    return JsonResponse({'success': False})
from django.shortcuts import render
from .models import Orders, Product  # Ensure Product is imported

def seller_orders_view(request):
    # Retrieve all orders
    orders = Orders.objects.all()  # You might want to filter this based on the seller or user

    # Optional: Retrieve the products related to the orders
    products = Product.objects.all()  # Get all products (or filter as needed)

    context = {
        'orders': orders,
        'products': products  # Add products to the context
    }

    return render(request, 'seller/seller_orders.html', context)

from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from .models import Orders

def update_order_status(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Orders, id=order_id)
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            order.save()
        return redirect(reverse('seller_orders'))  # Redirect to the dashboard

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from .models import Orders

def cancel_order(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    order.status = 'cancelled'
    order.save()
    
    messages.success(request, f'Order {order_id} has been cancelled successfully.')
    
    return redirect('view_orders')  # Adjust the redirect to your seller order page


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import User, Address

@login_required
def edit_profile(request):
    user = request.user
    # Get or create the user's address
    address, created = Address.objects.get_or_create(user=user)
    
    if request.method == "POST":
        # Update user fields
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        user.mobile_number = request.POST.get("mobile_number")
        user.save()

        # Update address fields
        address.address_line = request.POST.get("address_line")
        address.landmark = request.POST.get("landmark")
        address.city = request.POST.get("city")
        address.district = request.POST.get("district")
        address.pincode = request.POST.get("pincode")
        address.save()

        return redirect('checkout')  # Redirect to the checkout or success page

    return render(request, 'checkout.html', {'user': user, 'address': address})


from django.shortcuts import render, get_object_or_404
from .models import Orders

def order_info(request, order_id):
    order = get_object_or_404(Orders, id=order_id)
    return render(request, 'seller/order_details.html', {'order': order})

from django.shortcuts import render, get_object_or_404
from .models import Orders

def view_order(request, order_id):
    order = get_object_or_404(Orders, id=order_id)  # Returns 404 if order does not exist
    return render(request, 'seller/order_details.html', {'order': order})


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import CustomRequest  # Adjust with your model name

def generate_pdf_view(request):
    custom_requests = CustomRequest.objects.all()  # Query for your custom requests
    template_path = 'pdf_template.html'  # Path to your HTML template
    context = {'custom_requests': custom_requests}

    # Render the HTML template
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="custom_requests.pdf"'
    
    # Generate PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors with PDF generation')
    return response

import csv
from django.http import HttpResponse
from .models import Orders  # Adjust the import according to your app structure
def export_orders_csv(request):
    # Create the HttpResponse object with the appropriate CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(['Order ID', 'User', 'Seller', 'Payment Method', 'Created At', 'Amount', 'Product', 'Status', 'Quantity'])

    # Retrieve all orders and write them to the CSV
    for order in Orders.objects.all():
        writer.writerow([
            order.id,
            order.user.username,  # Assuming user has a username field
            order.seller.name if order.seller else 'N/A',  # Adjust according to your SellerProfile model
            order.payment_method,
            order.created_at,
            order.amount,
            order.product.product_name,  # Assuming Product model has a name field
            order.status,
            order.quantity,
        ])

    return response



# analytics/views.py

from django.shortcuts import render
from .models import Orders
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

def orders_chart_view(request):
    # Get the last 30 days of orders
    start_date = timezone.now() - timedelta(days=30)
    orders = Orders.objects.filter(created_at__gte=start_date)

    # Aggregate total amounts per day
    daily_totals = orders.values('created_at__date').annotate(total_amount=Sum('amount')).order_by('created_at__date')

    # Prepare data for the chart
    labels = []
    data = []
    for entry in daily_totals:
        labels.append(entry['created_at__date'].strftime('%Y-%m-%d'))
        data.append(float(entry['total_amount']))

    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'admin/orders_chart.html', context)


# ml_model.py
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
from store.models import Orders

def train_model():
    # Fetch your orders data
    orders = Orders.objects.values()  # You might want to filter or process this data
    df = pd.DataFrame(orders)

    # Prepare your features and target
    X = df[['quantity', 'amount']]  # Features: number of items and amount
    y = df['amount']  # Target: amount (or any other target variable)

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train model
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Save the model
    joblib.dump(model, 'sales_model.pkl')

train_model()
import pandas as pd
import numpy as np
from datetime import datetime, timedelta  # Add this line to import datetime and timedelta
from django.shortcuts import render
from .models import Orders
from sklearn.linear_model import LinearRegression
import plotly.graph_objs as go
import plotly.offline as pyo
def sales_analysis(request):
    # Get recent orders data (for the last 30 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    orders = Orders.objects.filter(created_at__range=[start_date, end_date])
    
    # Prepare data for analysis
    data = []
    for order in orders:
        data.append({
            'date': order.created_at.date(),  # Extract only the date
            'amount': order.amount,
            'quantity': order.quantity
        })
        
    df = pd.DataFrame(data)

    # Group by date and sum the amounts
    if not df.empty:
        df_grouped = df.groupby('date').sum().reset_index()  # Group by date only
        
        # Prepare Plotly graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_grouped['date'],
            y=df_grouped['amount'],
            mode='lines+markers',
            name='Historical Sales',
            line=dict(shape='linear'),
            marker=dict(size=6)
        ))
        
        # Prepare and add predictions
        X = np.array(range(len(df_grouped))).reshape(-1, 1)  # Features: Day index
        y = df_grouped['amount'].values  # Target: Sales amount
        
        # Train the model
        model = LinearRegression()
        model.fit(X, y)
        
        # Make predictions for the next 7 days
        future_days = np.array(range(len(df_grouped), len(df_grouped) + 7)).reshape(-1, 1)
        future_sales = model.predict(future_days)

        # Prepare future dates for predictions
        future_dates = pd.date_range(start=end_date + timedelta(days=1), periods=7).date
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=future_sales,
            mode='lines+markers',
            name='Predicted Sales',
            line=dict(dash='dash', color='red'),
            marker=dict(size=6)
        ))
        
        # Update layout
        fig.update_layout(
            title='Sales Analysis',
            xaxis_title='Date',
            yaxis_title='Sales Amount',
            template='plotly'
        )

        # Convert the figure to HTML
        plot_div = pyo.plot(fig, include_plotlyjs=False, output_type='div')
        
        return render(request, 'seller/sales_analysis.html', {'plot_div': plot_div})

    return render(request, 'seller/sales_analysis.html', {'plot_div': None})



from django.shortcuts import render, redirect, get_object_or_404
from .models import DeliveryAgent
from django.contrib import messages

# View to display the list of delivery agents
def view_delivery_staff(request):
    delivery_agents = DeliveryAgent.objects.all()  # Fetch all delivery agents
    return render(request, 'admin/view_delivery_staff.html', {'delivery_agents': delivery_agents})

# store/views.py

from django.core.mail import send_mail

def approve_delivery_agent(request, agent_id):
    agent = DeliveryAgent.objects.get(id=agent_id)
    agent.is_approved = True
    agent.save()

    # Send approval email
    subject = "Your Delivery Agent Profile is Approved!"
    message = f"Dear {agent.full_name},\n\nYour profile has been approved. You can now log in to your dashboard.\n\nThank you!"
    send_mail(subject, message, 'admin@yourwebsite.com', [agent.email])

    messages.success(request, "Delivery agent approved and notified via email.")
    return redirect('admin_dashboard')

# Reject delivery agent
def reject_delivery_agent(request, id):
    agent = DeliveryAgent.objects.get(id=id)
    agent.is_approved = False
    agent.is_pending = False
    agent.save()
    return redirect('delivery_staff')  # Redirect to the delivery staff list page



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Orders, DeliveryAgent

@login_required
def assign_order_to_delivery_agent(request):
    if not request.user.is_staff:  # Only allow staff/admin users to assign orders
        return redirect('home')  # Redirect non-staff users to the home page

    # Get the list of pending orders
    orders = Orders.objects.filter(status='Pending')  # Modify the filter as needed
    
    # Get all delivery agents
    delivery_agents = DeliveryAgent.objects.all()

    if request.method == 'POST':
        order_ids = request.POST.getlist('orders')  # Get the list of selected orders
        delivery_agent_id = request.POST.get('delivery_agent')  # Get the selected delivery agent
        
        if order_ids and delivery_agent_id:
            delivery_agent = DeliveryAgent.objects.get(id=delivery_agent_id)

            # Assign the selected delivery agent to the orders
            Orders.objects.filter(id__in=order_ids).update(delivery_agent=delivery_agent, status='Assigned')

            # Redirect to the same page with a success message
            return redirect('assign_orders')  # Redirect to the same page to show the update

    return render(request, 'assign_orders.html', {
        'orders': orders,
        'delivery_agents': delivery_agents,
    })

def get_places(request):
    district = request.GET.get("district", "").strip()
    print(f" Fetching places for district: {district}")  # Debugging

    if district:
        places = Place.objects.filter(preferred_district__iexact=district).values("id", "name").distinct()
        print(" Places found:", list(places))  # Debugging
        return JsonResponse(list(places), safe=False)
    
    return JsonResponse([], safe=False)  # Return empty list if district is missing


def view_assigned_agents(request):
    assignments = AgentDeliveryZone.objects.select_related('place', 'assigned_agent').all()
    return render(request, 'admin/view_assignagents.html', {'assignments': assignments})  

@login_required
def assign_delivery_agent_by_pincode(request):
    if not request.user.is_staff:  # Only allow staff/admin users to assign orders
        return redirect('index')  # Redirect non-staff users to the home page

    if request.method == 'POST':
        pincode = request.POST.get('pincode')  # Get the pincode from the form
        delivery_agent_id = request.POST.get('delivery_agent')  # Get the selected delivery agent

        # Get the list of pending orders for the given pincode
        orders = Orders.objects.filter(status='Pending', user__pincode=pincode)

        if delivery_agent_id:
            delivery_agent = DeliveryAgent.objects.get(id=delivery_agent_id)

            # Check if there are any orders to assign
            if orders.exists():
                # Assign the selected delivery agent to the orders
                for order in orders:
                    # Create a new DeliveryAssignment instance for each order
                    DeliveryAssignment.objects.create(order=order, delivery_agent=delivery_agent)

                    # Update the order's delivery agent and status if needed
                    order.delivery_agent = delivery_agent
                    order.status = 'Assigned'
                    order.save()

                messages.success(request, f'Delivery agent {delivery_agent.full_name} assigned to {orders.count()} orders.')
            else:
                messages.error(request, f'No pending orders found for pincode {pincode}.')

            return redirect('assign_delivery_agent_by_pincode')  # Redirect to the same page to show the update

    delivery_agents = DeliveryAgent.objects.all()  # Fetch all delivery agents
    return render(request, 'admin/assign_agent.html', {
        'delivery_agents': delivery_agents,
        'orders': orders if 'orders' in locals() else None,  # Pass orders if they exist
    })  
    
    
from django.shortcuts import render
from .models import DeliveryAgent

def delivery_agents_list(request):
    delivery_agents = DeliveryAgent.objects.all()
    return render(request, 'admin/view_delivery_staff.html', {'delivery_agents': delivery_agents})


from django.shortcuts import render, get_object_or_404
from .models import DeliveryAgent, Orders  # Ensure you import your models

def agent_assigned_orders(request, agent_id):
    # Fetch the delivery agent based on the provided agent_id
    agent = get_object_or_404(DeliveryAgent, id=agent_id)
    # Fetch the orders assigned to this agent
    assigned_orders = agent.orders.all()  # Assuming related_name='orders' in Orders model

    return render(request, 'delivery_agent/assigned_orders.html', {
        'agent': agent,
        'assigned_orders': assigned_orders,
    })
    
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import DeliveryAssignment

@login_required
def my_assigned_orders(request):
    # Ensure the user is a delivery agent
    if not hasattr(request.user, 'deliveryagent'):
        return render(request, 'delivery_agent/order_details.html', {'error': 'You are not a delivery agent'})

    delivery_agent = request.user.deliveryagent  # Get the logged-in delivery agent
    assigned_orders = DeliveryAssignment.objects.filter(delivery_agent=delivery_agent).order_by('-assigned_at')

    return render(request, 'delivery_agent/order_details.html', {'assigned_orders': assigned_orders})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt  # Temporarily disable CSRF protection for testing (remove in production)
def update_order_status(request, order_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            new_status = data.get("status", None)

            if not new_status:
                return JsonResponse({"error": "Missing status"}, status=400)

            order = Order.objects.filter(id=order_id).first()
            if not order:
                return JsonResponse({"error": "Order not found"}, status=404)

            order.status = new_status
            order.save()

            return JsonResponse({"success": "Order status updated successfully"})
        except Exception as e:
            print("Error updating order:", e)
            return JsonResponse({"error": "Something went wrong"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)



from django.shortcuts import render
from .models import Category

def custom_detail_view(request):
    categories = Category.objects.prefetch_related('subcategories').all()
    return render(request, 'custom.html', {'categories': categories})

from django.shortcuts import render
from .models import Category, SubCategory

def homepage(request):
    categories = Category.objects.prefetch_related('subcategory_set').all()
    return render(request, 'custom.html', {'categories': categories})



from django.shortcuts import render
from .models import CustomRequest

def custom_requests_list(request):
    requests = CustomRequest.objects.all()  # Fetch all custom requests
    return render(request, 'custom_requests_table.html', {'requests': requests})

from django.shortcuts import render
from .models import CustomRequest

def customization_requests_view(request):
    requests = CustomRequest.objects.all()  # Fetch all customization requests
    return render(request, 'designer/view_customization.html', {'requests': requests})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import CustomRequest  # Make sure this is your correct model
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CustomRequest  # Assuming your model is named CustomRequest

@login_required
def update_request_status(request, request_id):
    custom_request = get_object_or_404(CustomRequest, id=request_id)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["Pending", "Accepted"]:
            custom_request.status = new_status
            custom_request.save()
    return redirect("customization_requests")  # Redirect back to requests page


from django.shortcuts import render, get_object_or_404
from .models import CustomRequest

def customization_details(request, request_id):
    customization_request = get_object_or_404(CustomizationRequest, id=request_id)
    return render(request, 'designer/customization_details.html', {'request': customization_request})


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Material

@login_required
def add_material(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if name:
            material = Material(designer=request.user, name=name, description=description, image=image)
            material.save()
            messages.success(request, "Material added successfully!")
            return redirect('designer_dashboard')  # Redirect to designer's dashboard
        else:
            messages.error(request, "Material name is required.")

    return render(request, 'designer/add_material.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Material

@login_required
def view_materials(request):
    materials = Material.objects.filter(designer=request.user)  # Fetch only designer's materials
    return render(request, 'designer/view_materials.html', {'materials': materials})

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Furniture, FurnitureImage  # Import FurnitureImage for multiple images

def add_woodtype(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST.get("wood_description", "")
        price = request.POST.get("wood_price", "0")
        images = request.FILES.getlist("wood_images")  # Accept multiple images

        # ✅ Validate price format
        try:
            price = float(price)
        except ValueError:
            messages.error(request, "Invalid price format.")
            return redirect("add_material")

        # ✅ Save the wood type
        wood = Furniture(name=name, description=description, price=price)
        wood.save()

        # ✅ Save multiple images
        for image in images:
            FurnitureImage.objects.create(furniture=wood, image=image)

        messages.success(request, "Wood type added successfully!")
        return redirect("view_woodtype")

    return render(request, "designer/add_material.html")

from django.shortcuts import render, get_object_or_404, redirect
from .models import Furniture # Adjust model name if different

def view_woodtype(request):
    wood_types = Furniture .objects.all()
    return render(request, "designer/view_woodtype.html", {"wood_types": wood_types})

def delete_woodtype(request, wood_id):
    wood = get_object_or_404(Furniture , id=wood_id)
    wood.delete()
    return redirect("view_woodtype")  # Redirect back after deletion

from django.shortcuts import render, get_object_or_404, redirect
from .models import Furniture, FurnitureImage

def edit_furniture(request, id):
    furniture = get_object_or_404(Furniture, id=id)

    if request.method == 'POST':
        # Update furniture details
        furniture.name = request.POST.get('name')
        furniture.description = request.POST.get('description')
        furniture.price = request.POST.get('price')
        furniture.save()

        # Handle multiple images
        images = request.FILES.getlist('images')
        for image in images:
            FurnitureImage.objects.create(furniture=furniture, image=image)

        return redirect('view_woodtype')  # Redirect after saving

    images = FurnitureImage.objects.filter(furniture=furniture)
    return render(request, 'designer/edit_furniture.html', {'furniture': furniture, 'images': images})

def delete_furniture_image(request, image_id):
    image = get_object_or_404(FurnitureImage, id=image_id)
    furniture_id = image.furniture.id
    image.delete()
    return redirect('edit_furniture', id=furniture_id)


from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CustomizationRequest, Material, Furniture
from django.core.files.storage import FileSystemStorage

def customization_request_view(request):
   
    materials = Material.objects.all()
    wood_types = Furniture.objects.all()
    if request.method == 'POST':
        furniture_type = request.POST.get('furniture_type')

        customization = CustomizationRequest(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            furniture_type=furniture_type,
            material_id=request.POST.get('material'),
            wood_type_id=request.POST.get('wood_type'),
            color=request.POST.get('color'),
            finish=request.POST.get('finish'),
            storage_options=request.POST.get('storage_options'),
            special_features=request.POST.get('special_features'),
            reference_image=request.FILES.get('reference_image'),
            sketch_or_3d_model=request.FILES.get('sketch_or_3d_model'),
            expected_delivery_date=request.POST.get('expected_delivery_date') or None,
            urgent_request='urgent_request' in request.POST,  # ✅ This will work correctly
        )

        def get_decimal(value):
            return Decimal(value) if value else None

        if furniture_type == 'dining_table':
            customization.dining_length = get_decimal(request.POST.get('dining_length'))
            customization.dining_width = get_decimal(request.POST.get('dining_width'))
            customization.dining_height = get_decimal(request.POST.get('dining_height'))

        elif furniture_type == 'sofa':
            customization.sofa_length = get_decimal(request.POST.get('sofa_length'))
            customization.sofa_depth = get_decimal(request.POST.get('sofa_depth'))
            customization.sofa_seat_height = get_decimal(request.POST.get('sofa_seat_height'))

        elif furniture_type == 'bed':
            customization.bed_single_length = get_decimal(request.POST.get('bed_single_length'))
            customization.bed_single_width = get_decimal(request.POST.get('bed_single_width'))
            customization.bed_queen_length = get_decimal(request.POST.get('bed_queen_length'))
            customization.bed_queen_width = get_decimal(request.POST.get('bed_queen_width'))
            customization.bed_king_length = get_decimal(request.POST.get('bed_king_length'))
            customization.bed_king_width = get_decimal(request.POST.get('bed_king_width'))

        elif furniture_type == 'office_desk':
            customization.desk_length = get_decimal(request.POST.get('desk_length'))
            customization.desk_width = get_decimal(request.POST.get('desk_width'))
            customization.desk_height = get_decimal(request.POST.get('desk_height'))

        elif furniture_type == 'bookshelf':
            customization.bookshelf_height = get_decimal(request.POST.get('bookshelf_height'))
            customization.bookshelf_width = get_decimal(request.POST.get('bookshelf_width'))
            customization.bookshelf_depth = get_decimal(request.POST.get('bookshelf_depth'))

        elif furniture_type == 'wardrobe':
            customization.wardrobe_height = get_decimal(request.POST.get('wardrobe_height'))
            customization.wardrobe_width = get_decimal(request.POST.get('wardrobe_width'))
            customization.wardrobe_depth = get_decimal(request.POST.get('wardrobe_depth'))

        elif furniture_type == 'tv_unit':
            customization.tv_unit_length = get_decimal(request.POST.get('tv_unit_length'))
            customization.tv_unit_depth = get_decimal(request.POST.get('tv_unit_depth'))
            customization.tv_unit_height = get_decimal(request.POST.get('tv_unit_height'))

        elif furniture_type == 'coffee_table':
            customization.coffee_table_length = get_decimal(request.POST.get('coffee_table_length'))
            customization.coffee_table_width = get_decimal(request.POST.get('coffee_table_width'))
            customization.coffee_table_height = get_decimal(request.POST.get('coffee_table_height'))

        elif furniture_type == 'chair':
            customization.chair_seat_height = get_decimal(request.POST.get('chair_seat_height'))
            customization.chair_width = get_decimal(request.POST.get('chair_width'))
            customization.chair_depth = get_decimal(request.POST.get('chair_depth'))

        elif furniture_type == 'outdoor_bench':
            customization.bench_length = get_decimal(request.POST.get('bench_length'))
            customization.bench_depth = get_decimal(request.POST.get('bench_depth'))
            customization.bench_seat_height = get_decimal(request.POST.get('bench_seat_height'))

        customization.save()

    return render(request, "designer/customization_form.html", {"materials": materials, "wood_types": wood_types})
from django.shortcuts import render, get_object_or_404
from .models import CustomizationRequest

def customization_details(request, request_id):
    customization = get_object_or_404(CustomizationRequest, id=request_id)
    return render(request, 'customization_details.html', {'customization': customization})

from django.shortcuts import render
from .models import CustomizationRequest

def customization_requests_list(request):
    requests = CustomizationRequest.objects.all().order_by('-created_at')  # Fetch all requests sorted by date
    return render(request, 'designer/customization_requests_list.html', {'requests': requests})


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CustomizationRequest

@csrf_exempt
def update_status(request, request_id):
    """Update status of customization request via AJAX."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            status = data.get("status")

            customization_request = get_object_or_404(CustomizationRequest, id=request_id)
            customization_request.status = status
            customization_request.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request method"})

def edit_request(request, request_id):
    """Edit an existing customization request."""
    customization_request = get_object_or_404(CustomizationRequest, id=request_id)

    if request.method == "POST":
        customization_request.full_name = request.POST.get("full_name")
        customization_request.email = request.POST.get("email")
        customization_request.phone = request.POST.get("phone")
        customization_request.furniture_type = request.POST.get("furniture_type")
        customization_request.material_id = request.POST.get("material")
        customization_request.wood_type_id = request.POST.get("wood_type")
        customization_request.color = request.POST.get("color")
        customization_request.status = request.POST.get("status")
        customization_request.save()

        return redirect("customization_requests_list")  # Redirect to the requests page

    return render(request, "designer/edit_request.html", {"request": customization_request})

@csrf_exempt
def delete_request(request, request_id):
    """Delete a customization request via AJAX."""
    if request.method == "DELETE":
        try:
            customization_request = get_object_or_404(CustomizationRequest, id=request_id)
            customization_request.delete()
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})
    
    return JsonResponse({"success": False, "error": "Invalid request method"})


from store.models import CustomizationRequest

def user_customization_requests(request):
    requests = CustomizationRequest.objects.all()
    return render(request, 'designer/user_requests.html', {'requests': requests})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import CustomizationRequest, Payment

def payment_details(request, request_id):
    customization_request = get_object_or_404(CustomizationRequest, id=request_id)
    payment, created = Payment.objects.get_or_create(customization_request=customization_request)

    if request.method == "POST":
        payment.price_furniture = float(request.POST.get("price_furniture") or 0)
        payment.price_material = float(request.POST.get("price_material") or 0)
        payment.price_wood = float(request.POST.get("price_wood") or 0)
        payment.price_color = float(request.POST.get("price_color") or 0)
        payment.price_storage = float(request.POST.get("price_storage") or 0)
        payment.price_features = float(request.POST.get("price_features") or 0)
        payment.price_finish = float(request.POST.get("price_finish") or 0)
        payment.price_urgent = float(request.POST.get("price_urgent") or 0)
        payment.is_price_finalized = True  # Finalize price
        payment.save()
        messages.success(request, "Payment details saved successfully!")
        return redirect("customization_requests_list")

    return render(request, "designer/payment_details.html", {"request_obj": customization_request, "payment": payment})

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import CustomizationRequest, Payment

def download_invoice(request, request_id):  # Ensure request_id is received here
    customization_request = get_object_or_404(CustomizationRequest, id=request_id)
    payment = Payment.objects.filter(customization_request=customization_request).first()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="invoice_{request_id}.pdf"'

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setFont("Helvetica", 12)
    
    y = 750  # Start position

    pdf.drawString(100, y, "WoodCrest Customization Invoice")
    pdf.line(100, y - 5, 500, y - 5)
    
    y -= 30

    pdf.drawString(100, y, f"Customer Name: {customization_request.full_name}")
    pdf.drawString(100, y - 20, f"Request Date: {customization_request.created_at.strftime('%Y-%m-%d')}")
    pdf.drawString(100, y - 40, f"Furniture Type: {customization_request.get_furniture_type_display()}")
    pdf.drawString(100, y - 60, f"Material: {customization_request.material.name}")
    pdf.drawString(100, y - 100, f"Color: {customization_request.color}")

    y -= 140

    pdf.drawString(100, y, "Payment Details:")
    pdf.line(100, y - 5, 500, y - 5)
    y -= 30

    if payment:
        pdf.drawString(100, y, f"Furniture Price: ₹{payment.price_furniture or 0.00}")
        pdf.drawString(100, y - 20, f"Material Price: ₹{payment.price_material or 0.00}")
        pdf.drawString(100, y - 60, f"Color Price: ₹{payment.price_color or 0.00}")
        pdf.drawString(100, y - 80, f"Storage Price: ₹{payment.price_storage or 0.00}")
        pdf.drawString(100, y - 100, f"Special Features Price: ₹{payment.price_features or 0.00}")
        pdf.drawString(100, y - 120, f"Finish Price: ₹{payment.price_finish or 0.00}")
        pdf.drawString(100, y - 140, f"Urgent Request Price: ₹{payment.price_urgent or 0.00}") 
        pdf.drawString(100, y - 180, f"Total Price: ₹{payment.total_price}")
        pdf.line(100, y - 185, 500, y - 185)
    else:
        pdf.drawString(100, y, "Payment details not available.")

    pdf.save()
    return response


from django.shortcuts import render
from .models import CustomizationRequest, Payment

def dashboard_view(request):
    total_custom_orders = CustomizationRequest.objects.count()
    completed_designs = CustomizationRequest.objects.filter(status="Completed").count()
    pending_tasks = CustomizationRequest.objects.filter(status="Pending").count()
    customization_requests = CustomizationRequest.objects.exclude(status="Completed").count()  # Excludes completed ones

    context = {
        "total_custom_orders": total_custom_orders,
        "completed_designs": completed_designs,
        "pending_tasks": pending_tasks,
        "customization_requests": customization_requests,
    }
    
    return render(request, "designer/designer_dashboard.html", context)
