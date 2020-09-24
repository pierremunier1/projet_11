from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, Http404, JsonResponse
from users.models import CustomUser
from products.models import Product, Category, Substitute


def search(request):
    """showing the home page"""

    return render(request, "home.html")


def result(request):
    """show result page"""

    query = request.GET.get('query')

    try:
        product, substitutes = Product.objects.search_sub(query)
    except Product.DoesNotExist:
        messages.info(request, "Produit indisponible")
        return redirect("home")

    if not substitutes.exists():
        messages.info(request, "Substituts indisponible")
        return redirect("home")

    return render(
        request,
        "results.html",
        {
            "product": product,
            "substitutes": substitutes,
        }
    )


def detail(request, product_id):
    """show product detail"""

    product = Product.objects.get_detail(product_id)

    context = {
        'product': product.product_name,
        'brands': product.brands,
        'product_id': product.id,
        'thumbnail': product.image_food,
        'image_nutrition': product.image_nutrition,
        'url': product.product_url,
        'nutriscore_fr': product.nutriscore_fr,
    }

    return render(
        request,
        "detail.html",
        {
            "product": context
        }
    )


@login_required(login_url='/users/login/', redirect_field_name='next')
def save_substitute(request, product_original_id, product_substitute_id):
    """save substitute"""

    if request.user.is_authenticated:
        user = get_object_or_404(
            CustomUser,
            id=request.user.id
        )
        Substitute.objects.add_substitute(
            product_original_id, product_substitute_id, user
        )

        return redirect("favorite")


@login_required(login_url='/users/login/', redirect_field_name='next')
def favorite(request):
    """show favorite products"""

    products = Substitute.objects.filter(
        customuser=request.user
    )
    context = {
        "products": []
    }
    for product in products:
        context["products"].append([
            (
                product.product_original,
                Substitute.objects.filter(
                    product_original=product.product_original
                )
            ),
            (
                product.product_substitute,
                Substitute.objects.filter(
                    product_substitute=product.product_substitute
                )
            )
        ])
    return render(request, 'favorite.html', context)


@login_required(login_url='/users/login/?next=/favorite/', redirect_field_name='next')
def remove_products(request, product_original_id, product_substitute_id):
    """remove favorite"""

    user = CustomUser.objects.get(
        id=request.user.id
    )
    product_original = Product.objects.get(
        id=product_original_id
    )
    product_substitute = Product.objects.get(
        id=product_substitute_id
    )

    product = get_object_or_404(
        Substitute,
        customuser=user,
        product_original=product_original,
        product_substitute=product_substitute
    )
    product.delete()

    return redirect('favorite')


def mentions_legales(request):
    """Display the legal mentions of the site."""

    return render(request, 'mentions_legales.html')

@login_required(login_url='/users/login/?next=/my_account/', redirect_field_name='next')
def my_account(request):
    """account information."""
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, 'my_account.html', {'account': user})

def search_autocomplete(request):
    """autocomplete research in database"""
    products = list()
    if 'term' in request.GET:
        qs = (
            Product.objects.filter(
                product_name__icontains=request.GET.get('term')
                )[:5] or  
            Product.objects.filter(
                brands__icontains=request.GET.get('term')
                )[:5]
            )
        for product in qs:
            products.append(product.product_name)
    return JsonResponse(products, safe=False)
    
