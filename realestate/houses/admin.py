from django.contrib import admin
from .models import Property, Category
from parler.admin import TranslatableAdmin
from django.utils.translation import gettext_lazy as _


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)


@admin.register(Property)
class PropertyAdmin(TranslatableAdmin):
    list_display = ('get_title', 'city', 'price_per_night', 'available', 'room_count', 'square_meter', 'is_featured', 'created_at', 'category','status','owner')
    list_filter = ('room_count', 'is_featured', 'city')
    search_fields = ('translations__title', 'city')

    def get_title(self, obj):
        return obj.title
    get_title.admin_order_field = 'translations__title'  # Sıralama yapmak için
    get_title.short_description = _('title')  # Başlık olarak gösterilmesini sağlar