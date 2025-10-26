from django.contrib import admin
from .models import MenuItem

# Register your models here.
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'id','category', 'price', 'available')
    list_filter = ('available', 'category')
    search_fields = ('name',)
    ordering = ('name',)
    list_editable = ('price', 'available')

