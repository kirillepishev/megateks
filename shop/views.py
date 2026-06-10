from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from .models import Product, Category, Order, OrderItem


def get_cart_total(request):
    """Вычисляет общую сумму корзины"""
    cart = request.session.get('cart', {})
    if not cart:
        return 0
    
    total = 0
    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            total += product.price * quantity
        except Product.DoesNotExist:
            pass
    return total


def get_categories():
    """Получает все категории"""
    return Category.objects.all()


# Главная страница
def home(request):
    return render(request, 'shop/home.html', {
        'categories': get_categories(),
        'cart_total': get_cart_total(request),
    })


def catalog(request):
    products = Product.objects.filter(is_active=True)
    categories = get_categories()
    
    # Поиск
    query = request.GET.get('q')
    if query:
        products = products.filter(name__icontains=query)
    
    # Фильтр по категории
    category_id = request.GET.get('category')
    current_category = None
    if category_id:
        products = products.filter(category_id=category_id)
        current_category = get_object_or_404(Category, id=category_id)
    
    return render(request, 'shop/catalog.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'cart_total': get_cart_total(request),
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'categories': get_categories(),
        'cart_total': get_cart_total(request),
    })


def cart(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    
    total = 0
    cart_items = []
    for product in products:
        quantity = cart.get(str(product.id), 0)
        item_total = product.price * quantity
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total': item_total
        })
    
    return render(request, 'shop/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'categories': get_categories(),
        'cart_total': total,
    })


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    
    if product_id_str in cart:
        cart[product_id_str] += 1
    else:
        cart[product_id_str] = 1
    
    request.session['cart'] = cart
    return redirect('shop:cart')


@login_required
def checkout(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('shop:catalog')
        
        order = Order.objects.create(user=request.user, total_price=0)
        
        total = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_time=product.price
            )
            total += product.price * quantity
            product.stock_quantity -= quantity
            product.save()
        
        order.total_price = total
        order.save()
        request.session['cart'] = {}
        
        return redirect('shop:profile')
    
    return render(request, 'shop/checkout.html', {
        'categories': get_categories(),
        'cart_total': get_cart_total(request),
    })


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/profile.html', {
        'orders': orders,
        'categories': get_categories(),
        'cart_total': get_cart_total(request),
    })


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('shop:home')
    template_name = 'shop/register.html'