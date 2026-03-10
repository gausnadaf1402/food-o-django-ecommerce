from django.urls import path
from . import views

urlpatterns = [
    path('',views.product_list,name='home'),
path('product/<int:id>/',views.product_detail,name='product'),

path('register/',views.register,name='register'),
path('login/',views.login_view,name='login'),
path('logout/',views.logout_view,name='logout'),

path('cart/',views.cart,name='cart'),
path('add/<int:id>/',views.add_to_cart,name='add_to_cart'),
path('remove/<int:id>/',views.remove_cart,name='remove'),

path('checkout/',views.checkout,name='checkout'),
path('orders/',views.orders,name='orders'),

path('search/',views.search,name='search'),
# For Custom Dashboard
path('admin-products/',views.admin_products),
path('add-product/',views.add_product),
path('edit-product/<int:id>/',views.edit_product),
path('delete-product/<int:id>/',views.delete_product),

# Admin Dashboard
path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

#widhList URLs
path('wishlist/', views.wishlist, name='wishlist'),
path('add-to-wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
path('remove-from-wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
]
