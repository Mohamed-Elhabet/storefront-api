from django.contrib import admin
from core.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from store.admin import ProductAdmin, ProductImageInline
from tags.models import TaggedItem
from store.models import Product
from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.


# admin.site.register(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('username', 'password1', 'password2', 
                       'email', 'first_name', 'last_name')
        }),
    )

class TagInline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    


class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline, ProductImageInline]
    

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)

