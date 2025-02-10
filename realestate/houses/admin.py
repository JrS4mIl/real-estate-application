from django.contrib import admin
from .models import Property,Category
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','slug')
    search_fields=('name',)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display=('title','city','price_per_night','available','room_count','square_meter','is_featured','created_at','category',)
    list_filter=('room_count','is_featured','city')
    search_fields=('title','city')
