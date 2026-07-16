from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .models import Product, Category, Order, OrderItem
from .cart import Cart


def home(request):
    category_slug = request.GET.get('category')
    query = request.GET.get('q')

    products = Product.objects.all()
    categories = Category.objects.all()

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if query:
        products = products.filter(name__icontains=query)

    featured = Product.objects.filter(is_featured=True)[:4]

    context = {
        'products': products,
        'categories': categories,
        'featured': featured,
        'active_category': category_slug,
        'query': query or '',
    }
    return render(request, 'store/home.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
    })


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product=product, quantity=quantity)
    messages.success(request, f'Added "{product.name}" to your cart.')
    next_url = request.POST.get('next') or 'home'
    return redirect(next_url)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.info(request, f'Removed "{product.name}" from your cart.')
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('home')

    if request.method == 'POST':
        order = Order.objects.create(
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone_number=request.POST.get('phone_number'),
            address=request.POST.get('address'),
            district=request.POST.get('district'),
            pincode=request.POST.get('pincode'),
        )
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['price'],
                quantity=item['quantity'],
            )
        cart.clear()
        return render(request, 'store/order_success.html', {'order': order})

    return render(request, 'store/checkout.html', {'cart': cart})
