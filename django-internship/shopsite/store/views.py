from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from .models import Product
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.filter(name__icontains=query) if query else Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)  # 🔄 convert to string

    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1

    request.session['cart'] = cart
    return redirect('product_list')


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items, total = [], 0
    for pid, qty in cart.items():
        product = get_object_or_404(Product, id=pid)
        item_total = product.price * qty
        total += item_total
        cart_items.append({'product': product, 'quantity': qty, 'item_total': item_total})
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart.pop(str(product_id), None)
    request.session['cart'] = cart
    return redirect('view_cart')

def clear_cart(request):
    request.session['cart'] = {}
    return redirect('view_cart')  


def checkout(request):
    request.session['cart'] = {}
    return render(request, 'store/checkout.html')