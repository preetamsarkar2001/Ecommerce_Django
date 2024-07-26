from django.contrib import admin
from .models import*


admin.site.register(category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Slide)
admin.site.register(CartItem)
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)

admin.site.register(Review)