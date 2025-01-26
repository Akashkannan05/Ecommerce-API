from django.contrib import admin

from .models import ProductModel,CategoryModel,OrderItemModel,OrderModel,CartModel,ProfileModel

# Register your models here.

class PriceFilter(admin.SimpleListFilter):
    title=("Price List")
    parameter_name="Price List"

    def lookups(self, request, model_admin):
        return [
            ("0-100","0-100"),
            ("0-500","less than 500"),
            ('0-1000',"less than 1000"),
            ("0-5000","less than 5000"),
            ("0-10000","less than 10000"),
            (">10000","Greater than 10000")
        ]
    
    def queryset(self, request, queryset):
        if self.value()=="0-100":
            return queryset.filter(
                Price__gte=0,
                Price__lte=100
            )
        elif self.value()=="0-500":
            return queryset.filter(
                Price__gte=0,
                Price__lte=500
            )
        elif self.value()=="0-1000":
            return queryset.filter(
                Price__gte=0,
                Price__lte=1000
            )
        elif self.value()=="0-5000":
            return queryset.filter(
                Price__gte=0,
                Price__lte=5000
            )
        elif self.value()=="0-10000":
            return queryset.filter(
                Price__gte=10000
            )
        #return super().queryset(request, queryset)

class ProductAdmin(admin.ModelAdmin):
    #Want to keep price
    list_filter=('Category',PriceFilter)
    list_display=('Name','Price',"Inventory")
    search_fields = ('Name', 'Description')

admin.site.register(ProductModel,ProductAdmin)
admin.site.register(CategoryModel)

class OrderItemAdmin(admin.ModelAdmin):
    list_filter=('Order','Product') 
    list_display=('Product','Quantity')
admin.site.register(OrderItemModel,OrderItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_filter=('User','Status','OrderDate')
    list_display=('User','Status')
    search_fields = ('User__username', 'Status')

admin.site.register(OrderModel,OrderAdmin)

class CartAdmin(admin.ModelAdmin):
    list_filter = ('User', 'Product')
    list_display = ('User', 'Product', 'Quantity', 'Date')
    search_fields = ('User__username', 'Product__Name')

admin.site.register(CartModel,CartAdmin)
admin.site.register(ProfileModel)