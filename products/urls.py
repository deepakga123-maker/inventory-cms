from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    
    path(
    "products/<str:sku>/",
    views.product_detail,
    name="product_detail",
),

    path(
        "categories/<path:slug_path>/",
        views.category_detail,
        name="category_detail",
    ),
]