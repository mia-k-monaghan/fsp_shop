from django.contrib import admin
from . import models
from import_export import resources
from import_export.fields import Field
from import_export.admin import ImportExportModelAdmin
from django.utils.translation import gettext_lazy as _

# Register your models here.
class OrderResource(resources.ModelResource):
    class Meta:
        model=models.Order
        fields=['id',
        'product__title','product__stripe_id', 'product__includes_setup',
        'user','order_date']

@admin.register(models.Order)
class OrderAdmin(ImportExportModelAdmin):
    resource_class = OrderResource
    list_filter = ['product__includes_setup','setup_complete','product','order_date']
    search_fields = ['user','product__title','product__stripe_id','order_date']
    list_display = ['user','product','confirmed_email','setup_complete']
    list_display_links = ['user']

class ProductImageAdmin(admin.StackedInline):
    model = models.ProductImage
class ProductResource(resources.ModelResource):
    class Meta:
        model=models.Product
        fields=['id','stripe_id',
        'title','description','additional_details',
        'featured','archived', 'includes_setup']

class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    list_filter = ['featured','archived']
    search_fields = ['stripe_id','title']
    list_display = ['title','featured','archived']
    list_display_links = ['title']
    inlines = [ProductImageAdmin]

admin.site.register(models.Product,ProductAdmin)
