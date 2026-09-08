from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from .models import CategoryNode, Product
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory


class StockStatusFilter(admin.SimpleListFilter):
    title = "stock status"
    parameter_name = "stock_status"

    def lookups(self, request, model_admin):
        return (
            ("in_stock", "In Stock"),
            ("low_stock", "Low Stock"),
            ("out_of_stock", "Out of Stock"),
        )

    def queryset(self, request, queryset):
        if self.value() == "in_stock":
            return queryset.filter(quantity__gt=models.F("minimum_stock"))

        if self.value() == "low_stock":
            return queryset.filter(
                quantity__gt=0,
                quantity__lte=models.F("minimum_stock"),
            )

        if self.value() == "out_of_stock":
            return queryset.filter(quantity=0)

        return queryset

    
@admin.register(CategoryNode)
class CategoryNodeAdmin(TreeAdmin):
    form = movenodeform_factory(CategoryNode)
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sku",
        "category",
        "price",
        "quantity",
        "minimum_stock",
        "stock_status_display",
        "is_active",
    )
    def changelist_view(self, request, extra_context=None):
        low_stock_count = Product.objects.filter(
            quantity__gt=0,
            quantity__lte=models.F("minimum_stock"),
        ).count()

        extra_context = extra_context or {}
        extra_context["low_stock_count"] = low_stock_count

        return super().changelist_view(
            request,
            extra_context=extra_context,
        )     

    list_editable = ("quantity",)
   
    actions = ["mark_out_of_stock"]

    search_fields = (
    "name",
    "sku",
    "description",
    "category__name",
)

    list_filter = ("is_active", StockStatusFilter)

    @admin.action(description="Mark selected products as out of stock")
    def mark_out_of_stock(self, request, queryset):
        queryset.update(quantity=0)


    @admin.display(description="Stock Status")
    def stock_status_display(self, obj):
        if obj.stock_status == "Out of Stock":
            color = "red"
        elif obj.stock_status == "Low Stock":
            color = "orange"
        else:
            color = "green"

        return format_html(
            '<strong style="color: {};">{}</strong>',
            color,
            obj.stock_status,
        )