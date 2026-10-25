from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from decimal import Decimal


# ================= HOME =================

def home(request):

    products = Product.objects.all()

    return render(request, 'posApp/home.html', {
        'products': products
    })


# ================= PRODUCTS =================

def products(request):

    # Get all products
    product_list = Product.objects.all()

    # PRICE SORTING
    sort = request.GET.get('sort')

    if sort == 'low':
        # Low to High
        product_list = product_list.order_by('price')

    elif sort == 'high':
        # High to Low
        product_list = product_list.order_by('-price')

    else:
        # Default: Name
        product_list = product_list.order_by('name')

    return render(request, 'posApp/products.html', {
        'products': product_list
    })


# ================= ADD PRODUCT =================

def add_product(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        category = request.POST.get('category')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        Product.objects.create(
            name=name,
            category=category,
            price=price,
            quantity=quantity,
            description=description,
            image=image
        )

        return redirect('products')

    return render(request, 'posApp/add_product.html')


# ================= DELETE PRODUCT =================

def delete_product(request, id):

    product = get_object_or_404(Product, id=id)

    product.delete()

    return redirect('products')


# ================= ADD TO CART =================

def add_to_cart(request, id):

    product = get_object_or_404(Product, id=id)

    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')


# ================= CART =================

def cart(request):

    cart_data = request.session.get('cart', {})

    products = []

    total = Decimal('0.00')

    for product_id, quantity in cart_data.items():

        try:

            product = Product.objects.get(id=product_id)

            subtotal = product.price * quantity

            total += subtotal

            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

        except Product.DoesNotExist:
            pass

    return render(request, 'posApp/cart.html', {
        'cart_products': products,
        'total': total
    })


# ================= REMOVE FROM CART =================

def remove_from_cart(request, id):

    cart = request.session.get('cart', {})

    product_id = str(id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')


# ================= CHECKOUT =================

def checkout(request):

    cart_data = request.session.get('cart', {})

    products = []

    total = Decimal('0.00')

    for product_id, quantity in cart_data.items():

        try:

            product = Product.objects.get(id=product_id)

            subtotal = product.price * quantity

            total += subtotal

            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })

        except Product.DoesNotExist:
            pass

    if not products:
        return redirect('products')

    return render(request, 'posApp/checkout.html', {
        'cart_products': products,
        'total': total
    })


# ================= PLACE ORDER =================

def place_order(request):

    if request.method != 'POST':
        return redirect('checkout')

    cart_data = request.session.get('cart', {})

    if not cart_data:
        return redirect('products')

    customer_name = request.POST.get('customer_name')
    phone = request.POST.get('phone')
    address = request.POST.get('address')

    total = Decimal('0.00')

    cart_products = []

    for product_id, quantity in cart_data.items():

        try:

            product = Product.objects.get(id=product_id)

            subtotal = product.price * quantity

            total += subtotal

            cart_products.append({
                'product': product,
                'quantity': quantity
            })

        except Product.DoesNotExist:
            pass

    # ================= CREATE ORDER =================

    order = Order.objects.create(
        customer_name=customer_name,
        phone=phone,
        address=address,
        total_amount=total
    )

    # ================= CREATE ORDER ITEMS =================

    for item in cart_products:

        OrderItem.objects.create(
            order=order,
            product=item['product'],
            quantity=item['quantity'],
            price=item['product'].price
        )

    # ================= CLEAR CART =================

    request.session['cart'] = {}

    return render(request, 'posApp/order_success.html', {
        'order': order
    })