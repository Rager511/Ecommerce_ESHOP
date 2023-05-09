from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Category, Product, Commande, CustomUser, Payment

admin.site.site_header = "E-commerce"
admin.site.site_title = "E-Shop"
admin.site.index_title = "Manager"

class AdminCategorie(admin.ModelAdmin):
    list_display = ('name', 'date_added')

class AdminProduct(admin.ModelAdmin):
    list_display = ('title', 'price', 'category', 'date_added')
    search_fields = ('title',)
    list_editable = ('price',)
    ordering = ('date_added',)

class AdminCommande(admin.ModelAdmin):
    list_display = ('items','nom','email','address', 'ville', 'pays','total', 'date_commande')

class AdminPayment(admin.ModelAdmin):
    list_display = ('amount', 'date')

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'city', 'country')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Product, AdminProduct)
admin.site.register(Category, AdminCategorie)
admin.site.register(Commande, AdminCommande)
admin.site.register(Payment, AdminPayment)
