from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

def index_view(request):
    return render(request, 'index.html')


def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product-single.html', {'product': product})


def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, 'shop.html', {'products': products})


def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]['quantity']
        subtotal = quantity * product.get_net_price()
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })



def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
    return redirect('cart')


def add_to_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('product-quantity', 1))
        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id]['quantity'] += quantity
        else:
            cart[product_id] = {'quantity': quantity}

        request.session['cart'] = cart
        request.session.modified = True
        return redirect('cart')
    else:
        return redirect('shop')


from django.shortcuts import render, redirect
from .models import Product, Order, OrderItem
from django.contrib import messages

def checkout_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    cart_items = []
    total = 0

    for product in products:
        quantity = cart[str(product.id)]['quantity']
        subtotal = quantity * product.get_net_price()
        total += subtotal
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')

        # Save order
        order = Order.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            zip_code=zip_code,
            total_price=total
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['product'].get_net_price()
            )

        # Clear cart
        request.session['cart'] = {}
        request.session.modified = True

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('index')  # or redirect to a 'thank you' page

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total': total
    })
