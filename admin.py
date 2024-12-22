from django.contrib import admin
from .models import Cart,Customer, OrderPlaced, Payment, Product, Wishlist
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import Group
@admin.register(Product)
# Register your models here.
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id','title','discounted_price','category','product_image']

@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','locality','city','state','zipcode']

@admin.register(Cart)
class CartModelAdmin (admin.ModelAdmin):
    list_display= ['id', 'user', 'product', 'quantity']
    def products(self,obj):
        link = reverse("admin:app1_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'paypal_payment_id', 'paid')

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id','user','customers','products','quantity','ordered_date','status','payment']
    def customers(self,obj):
        link=reverse('admin:app1_customer_change', args=[obj.customer.pk])
        return format_html('<a href="{}">{}</a>', link, obj.customer.name)
    
    def products(self,obj):
        link=reverse('admin:app1_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)
    
    def payments(self, obj):
        link = reverse('admin:app1_payment_change', args=[obj.payment.pk])
        return format_html('<a href="{}">{}</a>', link, obj.payment.paypal_payment_id)

@admin.register(Wishlist)
class WishlistModelAdmin (admin.ModelAdmin):
    list_display = ['id', 'user', 'product']
    def products(self,obj):
        link = reverse("admin:app1_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', link, obj.product.title)

admin.site.unregister(Group)

