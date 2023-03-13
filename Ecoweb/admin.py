from django.contrib import admin
from .models import Item, OrderItem, Order


class itemAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "photo"]


admin.site.register(Item, itemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
