from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import seller_dashboard_view  
from .views import view_sellers  
from .views import delivery_dashboard
from .views import create_custom_request, custom_view,seller_page

from.import views
urlpatterns = [
    path('login/', views.login_view, name='login'),  # Login view URL
    path('register/', views.register, name='register'),  # Registration view URL
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),  # Admin dashboard URL
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),  # Seller dashboard URL
    path('', views.index, name='index'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
     path('logout/', views.logout_view, name='logout'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('view-customers/', views.view_customers, name='view_customers'),
    path('view-subcategories/', views.view_subcategories, name='view_subcategories'),
    path('add-category/', views.add_category, name='add_category'),
     path('edit-category/<int:category_id>/', views.edit_category, name='edit_category'),
    path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('add-subcategory/', views.add_subcategory, name='add_subcategory'),
    path('view-subcategories/', views.view_subcategories, name='view_subcategories'),
    path('edit-subcategory/<int:id>/', views.edit_subcategory, name='edit_subcategory'),
    path('delete-subcategory/<int:id>/', views.delete_subcategory, name='delete_subcategory'),
    path('view-subcategories/', views.view_subcategories, name='view_subcategories'),
    path('toggle-status/<int:category_id>/', views.toggle_status, name='toggle_status'),  # URL for toggling status
    path('blocked/', views.blocked_view, name='blocked'),
    path('view-category/', views.view_category, name='view_category'),
    path('toggle-subcategory-status/<int:subcategory_id>/',views.toggle_subcategory_status, name='toggle_subcategory_status'),
    path('toggle-customer-status/<int:user_id>/', views.toggle_customer_status, name='toggle_customer_status'),
    path('seller/categories/', views.seller_view_categories, name='seller_view_categories'),
    path('seller/subcategories/', views.seller_view_subcategories, name='seller_view_subcategories'),
    path('add-product/', views.add_product_view, name='add_product'),
    path('view-products/', views.view_product, name='view_product'),
    path('products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('seller/dashboard/', views.seller_dashboard_view, name='seller_dashboard'),
    path('search/', views.search_products, name='search_products'),
    path('category/<str:category_name>/',views.category_display, name='category_display'),
    path('subcategory/<int:subcategory_id>/', views.subcategory_detail, name='subcategory_detail'),
    path('sellers/', views.view_sellers, name='view_sellers'),  # Add this line
    path('views-products/', views.view_seller_products, name='views_product'),
    path('blocked/', views.blocked_view, name='blocked'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'), 
    path('profile/', views.seller_profile, name='seller_profile'),
    path('view-seller/<int:seller_id>/', views.view_seller, name='view_seller'),
    path('sellers/approve/<int:seller_id>/', views.approve_seller, name='approve_seller'),
    path('sellers/pending/<int:seller_id>/', views.pending_seller, name='pending_seller'),
    path('sellers/reject/<int:seller_id>/', views.reject_seller, name='reject_seller'),
    path('reject-seller/<int:seller_id>/', views.reject_seller, name='reject_seller'),
    path('sellers/pending/<int:seller_id>/', views.pending_seller, name='pending_seller'),
    path('custom/', views.custom_view, name='custom'),
    path('create_custom_request/', views.create_custom_request, name='create_custom_request'),
    path('create_custom_request/', views.create_custom_requests, name='create_custom_request'),
    path('seller/', views.seller_page, name='seller_page'),
    path('categories/', views.category_view, name='category_view'),
    path('products/', views.product_list, name='product_list'),
    path('products/', views.product_list_view, name='product_list_view'),
    path('submit_comment/', views.submit_comment, name='submit_comment'),
    path('seller_comments/', views.seller_comments, name='seller_comments'),
    path('admin_comments/', views.admin_comments, name='admin_comments'),
    path('', views.index, name='index'),  # Home page URL pattern
    path('thank-you/', views.thank_you_view, name='thank_you'),
    path('place_order/', views.place_order, name='place_order'),
    path('order/<int:order_id>/', views.view_order, name='view_order'),

    path('payment-success/', views.payment_success, name='payment_success'),

    path('wishlist/add/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

    path('orders/', views.view_orders, name='view_orders'),  # URL for listing orders
    path('orders/<int:order_id>/', views.order_details, name='order_details'),  # URL for order details
    
    path('orders/', views.my_orders, name='my_orders'),
    path('orders/search/', views.my_orders, name='order_search'), 
    
     path('contact/', views.contact_view, name='contact_view'),
    path('submit-rating/<int:order_id>/', views.submit_rating, name='submit_rating'),
    
    path('orders/remove/<int:order_id>/', views.remove_order, name='remove_order'),
    path('seller/orders/', views.seller_orders_view, name='seller_orders'),

    path('update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('order/<int:order_id>/', views.order_info, name='order_info'),

    path('generate-pdf/', views.generate_pdf_view, name='generate_pdf'),
    path('export-orders-csv/', views.export_orders_csv, name='export_orders_csv'),
    path('sales-analysis/', views.sales_analysis, name='sales_analysis'),  # URL for sales analysis
    path('orders/chart/', views.orders_chart_view, name='orders_chart'),
    

# store/urls.py


    path('delivery-staff/', views.view_delivery_staff, name='delivery_staff'),
    path('delivery_dashboard/', views.delivery_dashboard, name='delivery_dashboard'),
    path("complete-profile/", views.complete_profile_view, name="complete_profile"),
    path('delivery-staff/', views.view_delivery_staff, name='view_delivery_staff'),
    path('approve_delivery_agent/<int:agent_id>/', views.approve_delivery_agent, name='approve_delivery_agent'),
    path('reject_delivery_agent/<int:id>/', views.reject_delivery_agent, name='reject_delivery_agent'),
    path("get-places/", views.get_places, name="get_places"),    
    path('view-assigned-agents/', views.view_assigned_agents, name='view_assigned_agents'),
    path('assign-delivery-agent/', views.assign_delivery_agent_by_pincode, name='assign_delivery_agent_by_pincode'),
    path('delivery-agents/', views.delivery_agents_list, name='delivery_agents_list'),
    path('dashboard/', views.my_assigned_orders, name='my_assigned_orders'),
    path('update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),

    path('designer/dashboard/', views.designer_dashboard, name='designer_dashboard'),
    path('designer-dashboard/', views.designer_dashboard, name='designer_dashboard'),  
    path('custom/', views.custom_detail_view, name='custom'),
    path('category/<str:category_name>/', views.category_display, name='category_display'),
    path('custom-requests/', views.custom_requests_list, name='custom_requests_list'),
    path('customization-requests/', views.customization_requests_view, name='customization_requests'),
    path('update-request-status/<int:request_id>/', views.update_request_status, name='update_request_status'),
    path('customization/<int:request_id>/', views.customization_details, name='customization_details'),
    path('add-material/', views.add_material, name='add_material'),
    path('designer/view-materials/', views.view_materials, name='view_materials'),
    path("add-woodtype/", views.add_woodtype, name="add_woodtype"),
    path("view-woodtype/", views.view_woodtype, name="view_woodtype"),
    path("delete-woodtype/<int:wood_id>/", views.delete_woodtype, name="delete_woodtype"),
    path('furniture/edit/<int:id>/', views.edit_furniture, name='edit_furniture'),
    path('furniture/delete-image/<int:image_id>/', views.delete_furniture_image, name='delete_furniture_image'),
    path('customization-request/', views.customization_request_view, name='customization_request'),
    path('customization-requests_list/', views.customization_requests_list, name='customization_requests_list'),
    path("update_status/<int:request_id>/", views.update_status, name="update_status"),
    path("edit_request/<int:request_id>/", views.edit_request, name="edit_request"),
    path("delete_request/<int:request_id>/", views.delete_request, name="delete_request"),
    path('my-requests/', views.user_customization_requests, name='user_customization_requests'),
    path('payment_details/<int:request_id>/', views.payment_details, name='payment_details'),
    path('download-invoice/<int:request_id>/', views.download_invoice, name='download_invoice'),

    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


