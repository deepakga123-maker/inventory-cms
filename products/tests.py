from django.test import TestCase

from .models import CategoryNode, Product


class ProductModelTests(TestCase):
    def setUp(self):
        self.category = CategoryNode.add_root(
            name="Electronics",
            slug="electronics",
        )

    def test_product_string_returns_name(self):
        product = Product.objects.create(
            name="Wireless Mouse",
            sku="WM-001",
            category=self.category,
            price=699,
            quantity=5,
            minimum_stock=5,
        )

        self.assertEqual(str(product), "Wireless Mouse")

    def test_stock_status_in_stock(self):
        product = Product.objects.create(
            name="Keyboard",
            sku="KB-001",
            category=self.category,
            price=2499,
            quantity=10,
            minimum_stock=5,
        )

        self.assertEqual(product.stock_status, "In Stock")

    def test_stock_status_low_stock(self):
        product = Product.objects.create(
            name="Mouse",
            sku="MS-001",
            category=self.category,
            price=699,
            quantity=5,
            minimum_stock=5,
        )

        self.assertEqual(product.stock_status, "Low Stock")

    def test_stock_status_out_of_stock(self):
        product = Product.objects.create(
            name="Headphones",
            sku="HP-001",
            category=self.category,
            price=1499,
            quantity=0,
            minimum_stock=5,
        )

        self.assertEqual(product.stock_status, "Out of Stock")

class ProductViewTests(TestCase):
    def setUp(self):
        self.electronics = CategoryNode.add_root(
            name="Electronics",
            slug="electronics",
        )

        self.accessories = self.electronics.add_child(
            name="Accessories",
            slug="accessories",
        )

        self.mice = self.accessories.add_child(
            name="Mice",
            slug="mice",
        )

        self.product = Product.objects.create(
            name="Wireless Mouse",
            sku="WM-001",
            description="Ergonomic wireless mouse for office use",
            category=self.mice,
            price=699,
            quantity=5,
            minimum_stock=5,
            is_active=True,
        )        

    def test_product_list_page(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Mouse")    

    def test_search_by_product_name(self):
        response = self.client.get("/", {"q": "mouse"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Mouse")

    def test_search_by_description(self):
        response = self.client.get("/", {"q": "ergonomic"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Mouse")    

    def test_search_by_parent_category(self):
        response = self.client.get("/", {"q": "Accessories"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Mouse")   

    def test_product_detail_page(self):
        response = self.client.get(f"/products/{self.product.sku}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Mouse")
        self.assertContains(response, "Ergonomic wireless mouse")

    def test_category_detail_page(self):
        response = self.client.get("/categories/electronics/accessories/mice/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Wireless Mouse")      