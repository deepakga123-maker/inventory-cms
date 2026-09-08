from django.db import models
from treebeard.mp_tree import MP_Node


class CategoryNode(MP_Node):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150)

    def get_slug_path(self):
        categories = list(self.get_ancestors()) + [self]
        return "/".join(category.slug for category in categories)

    def get_ancestors_and_self(self):
        return list(self.get_ancestors()) + [self]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "category node"
        verbose_name_plural = "category nodes"

class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    category = models.ForeignKey(
       CategoryNode,
       on_delete=models.SET_NULL,
       null=True,
       blank=True,
       related_name="products",
)

    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    minimum_stock = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def stock_status(self):
        if self.quantity == 0:
            return "Out of Stock"
        elif self.quantity <= self.minimum_stock:
            return "Low Stock"
        return "In Stock"

    def __str__(self):
        return self.name