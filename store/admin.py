from django.contrib import admin
from .models import AdminPanel,UserProfile,Category,Product,Cart

admin.site.register(AdminPanel)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)