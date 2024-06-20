from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.http import HttpRequest
from . import models
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from tags.models import TaggedItem
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    autocomplete_fields = ['featured_product']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # return collection.products_count
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            })
        )
        return format_html('<a href="{}">{}</a>',
                           url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count=Count('products')
        )


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<10', 'Low')
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        
        


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ['thumbnail']
    
    def thumbnail(self, instance):
        if instance.image.name != '':
            return format_html(
                f'<img src="{instance.image.url}" class="thumbnail" />'
            )
        return ''
    
        
        


# class TagInline(GenericTabularInline):
#     autocomplete_fields = ['tag']
#     model = TaggedItem




@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # inlines = [TagInline]
    # fields = ['title', 'slug']
    # exclude = ['promotions']
    # readonly_fields = ['title']
    prepopulated_fields = {
        'slug': ['title']
    }
    search_fields = ['title']
    autocomplete_fields = ['collection']
    list_display = ['title', 'unit_price', 'inventory_status',
                    'collection', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    list_filter = ['collection', 'last_update', InventoryFilter]
    actions = ['clear_inventory']
    inlines = [ProductImageInline]

    def collection_title(self, product):
        # return product.collection.title
        try:
            label = product.collection.title
        except:
            label = '..'
        return label

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )
        
    
    class Media:
        css = {
            'all': ['store/styles.css']
        }


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    list_editable = ['membership']
    ordering = ['user__first_name', 'user__last_name']
    list_select_related = ['user']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    autocomplete_fields = ['user']

    def orders(self, customer):
        # return customer.order_set.all()
        url = (
            reverse('admin:store_order_changelist')
            + '?'
            + urlencode({
                'customer__id': str(customer.id)
            })
        )
        return format_html('<a href="{}">{}</a>',
                           url, customer.order_set.all().count())



class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 0
    min_num = 1
    max_num = 10



@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]


    