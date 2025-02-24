

# Register your models here.
from django.contrib import admin
from .models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_featured')
    list_filter = ('is_featured',)
    search_fields = ('user__username', 'user__email')

admin.site.register(Profile, ProfileAdmin)
