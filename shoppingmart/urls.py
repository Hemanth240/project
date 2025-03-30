from django.conf import settings
from django.urls import path
from store import views
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),  # ✅ Renamed to user_login
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),


    # Cart and Checkout
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
]

urlpatterns = [
    path('admin/', admin.site.urls),  # ✅ This must be present
    path('', include('store.urls')),
]

# ✅ Serve Media Files (Profile Images, Product Images, etc.)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)