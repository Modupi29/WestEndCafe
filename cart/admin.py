from django.contrib import admin
from .models import CartItem

# Register your models here.

@admin.register(CartItem)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'quantity')
    search_fields = ('user__username', 'item__name')
    list_editable = ('quantity',)
    raw_id_fields = ('user', 'item')

