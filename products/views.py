from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from .models import CategoryNode, Product


def product_list(request):
    products = Product.objects.filter(
        is_active=True
    ).order_by("name")

    query = request.GET.get("q", "").strip()

    if query:
        search_vector = (
            SearchVector("name", weight="A")
            + SearchVector("sku", weight="A")
            + SearchVector("description", weight="B")
        )

        search_query = SearchQuery(query)

        category_q = Q(pk__in=[])

        matching_categories = CategoryNode.objects.filter(
            name__icontains=query
        )

        for category in matching_categories:
            category_q |= Q(
                category__path__startswith=category.path
            )

        products = (
            products
            .annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query),
            )
            .filter(
                Q(search=search_query) | category_q
            )
            .order_by("-rank", "name")
            .distinct()
        )

    paginator = Paginator(products, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "products/product_list.html", {
        "products": page_obj,
        "page_obj": page_obj,
        "query": query,
    })

def product_detail(request, sku):
    product = get_object_or_404(
        Product,
        sku=sku,
        is_active=True,
    )

    if product.category:
        breadcrumbs = product.category.get_ancestors_and_self()
    else:
        breadcrumbs = []

    return render(request, "products/product_detail.html", {
        "product": product,
        "breadcrumbs": breadcrumbs,
    })


def category_detail(request, slug_path):
    normalized_path = slug_path.strip("/")

    last_slug = normalized_path.split("/")[-1]

    category = None

    for candidate in CategoryNode.objects.filter(slug=last_slug):
        if candidate.get_slug_path() == normalized_path:
            category = candidate
            break

    if category is None:
        raise Http404("Category not found")

    descendant_categories = list(category.get_descendants())
    descendant_categories.append(category)

    products = Product.objects.filter(
        category__in=descendant_categories,
        is_active=True,
    ).order_by("name")

    children = category.get_children()

    breadcrumbs = category.get_ancestors_and_self()

    return render(request, "products/category_detail.html", {
        "category": category,
        "products": products,
        "children": children,
        "breadcrumbs": breadcrumbs,
    })