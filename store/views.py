from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from .models import Product, Category, Order, OrderItem, Wishlist, Review


def get_cart(request):
    return request.session.get('cart', {})


def save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def home(request):
    featured = Product.objects.filter(is_featured=True, stock__gt=0)[:8]
    new_arrivals = Product.objects.filter(is_new_arrival=True, stock__gt=0)[:8]
    ladies_cats = Category.objects.filter(audience__in=['ladies', 'both'])[:4]
    kids_cats = Category.objects.filter(audience__in=['kids', 'both'])[:4]
    return render(request, 'store/home.html', {
        'featured': featured, 'new_arrivals': new_arrivals,
        'ladies_cats': ladies_cats, 'kids_cats': kids_cats,
    })


def shop(request):
    products = Product.objects.filter(stock__gt=0)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    audience = request.GET.get('audience')
    search = request.GET.get('search', '')
    sort = request.GET.get('sort', 'newest')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_slug:
        products = products.filter(category__slug=category_slug)
    if audience:
        products = products.filter(category__audience__in=[audience, 'both'])
    if search:
        products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    else:
        products = products.order_by('-created_at')

    return render(request, 'store/shop.html', {
        'products': products, 'categories': categories,
        'selected_category': category_slug, 'selected_audience': audience,
        'search': search, 'sort': sort,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    reviews = product.reviews.select_related('user').order_by('-created_at')
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    in_wishlist = Wishlist.objects.filter(user=request.user, product=product).exists() if request.user.is_authenticated else False

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.update_or_create(product=product, user=request.user,
                defaults={'rating': rating, 'comment': comment})
            messages.success(request, 'Review submitted!')
            return redirect('product_detail', slug=slug)

    return render(request, 'store/product_detail.html', {
        'product': product, 'reviews': reviews,
        'avg_rating': round(avg_rating, 1), 'related': related, 'in_wishlist': in_wishlist,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    size = request.POST.get('size', '')
    qty = int(request.POST.get('quantity', 1))
    cart = get_cart(request)
    key = f"{product_id}_{size}"
    if key in cart:
        cart[key]['quantity'] += qty
    else:
        cart[key] = {
            'product_id': product_id, 'name': product.name,
            'price': str(product.price),
            'image': product.image.url if product.image else '',
            'size': size, 'quantity': qty,
        }
    save_cart(request, cart)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': sum(i['quantity'] for i in cart.values())})
    messages.success(request, f'"{product.name}" added to cart!')
    return redirect('cart')


def cart(request):
    cart = get_cart(request)
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'store/cart.html', {'cart': cart, 'total': total})


def remove_from_cart(request, key):
    cart = get_cart(request)
    if key in cart:
        del cart[key]
        save_cart(request, cart)
    return redirect('cart')


def update_cart(request, key):
    cart = get_cart(request)
    qty = int(request.POST.get('quantity', 1))
    if key in cart:
        if qty > 0:
            cart[key]['quantity'] = qty
        else:
            del cart[key]
        save_cart(request, cart)
    return redirect('cart')


def checkout(request):
    cart = get_cart(request)
    if not cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('shop')
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key or '',
            full_name=request.POST['full_name'], email=request.POST['email'],
            phone=request.POST['phone'], address=request.POST['address'],
            city=request.POST['city'], state=request.POST['state'],
            pincode=request.POST['pincode'], total_amount=total,
        )
        for key, item in cart.items():
            product = Product.objects.filter(id=item['product_id']).first()
            OrderItem.objects.create(
                order=order, product=product, product_name=item['name'],
                size=item.get('size', ''), quantity=item['quantity'], price=item['price'],
            )
        save_cart(request, {})
        return redirect('order_success', order_id=order.id)
    return render(request, 'store/checkout.html', {'cart': cart, 'total': total})


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items')
    wishlist = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/profile.html', {'orders': orders, 'wishlist': wishlist})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    obj, created = Wishlist.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'in_wishlist': created})
    messages.success(request, 'Wishlist updated!')
    return redirect('product_detail', slug=product.slug)


def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST.get('email', '')
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, f'Welcome to Febz Couture, {username}!')
            return redirect('home')
    return render(request, 'store/auth.html', {'mode': 'register'})


def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'store/auth.html', {'mode': 'login'})


def logout_view(request):
    logout(request)
    return redirect('home')
