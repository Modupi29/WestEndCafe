from django.shortcuts import render, redirect, get_object_or_404
from .models import CartItem, Cart, Order, OrderItem
from menu.models import MenuItem
from .forms import CartAddForm,PaymentProofForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from order.models import Order as MainOrder
from django.utils import timezone


# Create your views here.

def cart_detail(request):
    if not request.user.is_authenticated:
        return redirect('login')  # or wherever you want

    # Get or create cart for the current user
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Get all items in the cart
    cart_items = CartItem.objects.filter(user=request.user).select_related('item')

    # Calculate total price
    total_price = sum(item.get_total_price() for item in cart_items)

    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart': cart
    })

@login_required
def cart_add(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(MenuItem, id=item_id)
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            item=item,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        # Return current total number of items in the cart
        cart_count = CartItem.objects.filter(user=request.user).count()
        return JsonResponse({
            'message': f'{item.name} added to cart!',
            'cart_count': cart_count
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def cart_delete(request, item_id):
    CartItem.objects.filter(id=item_id, user=request.user).delete()
    return redirect('cart_detail')


@login_required
def cart_update(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get(f'quantity_{item_id}', 1))
        cart_item = CartItem.objects.filter(id=item_id, user=request.user).first()
        if cart_item:
            cart_item.quantity = max(quantity, 1)
            cart_item.save()
    return redirect('cart_detail')

@login_required
def pay_now(request):
    if request.method == 'POST':
        form = PaymentProofForm(request.POST, request.FILES)
        if form.is_valid():
            # Get cart items
            cart_items = CartItem.objects.filter(user=request.user)
            if not cart_items.exists():
                return JsonResponse({'success': False, 'message': 'Your cart is empty.'})

            # Validate file
            file = request.FILES.get('file')
            if not file:
                return JsonResponse({'success': False, 'message': 'No file uploaded.'})
            if not file.name.lower().endswith(('.pdf', '.jpg', '.jpeg')):
                return JsonResponse({'success': False, 'message': 'Only PDF or JPG files are allowed.'})

            # Create order
            order = Order.objects.create(
                user=request.user,
                order_date=timezone.now(),
                total_items=sum(ci.quantity for ci in cart_items),
                total_price=sum(ci.item.price * ci.quantity for ci in cart_items),
                status='Paid'
            )

            # Add order items
            for ci in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu_item=ci.item,
                    quantity=ci.quantity,
                    price=ci.item.price
                )

            # Save payment proof
            payment_proof = form.save(commit=False)
            payment_proof.user = request.user
            payment_proof.order = order
            payment_proof.save()

            # Clear cart
            cart_items.delete()

            return JsonResponse({'success': True, 'message': 'Payment proof uploaded and order placed successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid form submission.'})

    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

@login_required
def pay_later(request):
    if request.method == "POST":
        cart_items = CartItem.objects.filter(user=request.user)
        if cart_items.exists():
            # Create an order
            order = Order.objects.create(user=request.user, status='Pending')
            order.items.set(cart_items)  # Assuming Order has a ManyToMany to CartItem
            # Optionally, clear cart
            cart_items.delete()
            return JsonResponse({'success': True, 'message': 'Order saved as Pay Later!'})
        return JsonResponse({'success': False, 'message': 'Cart is empty.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def checkout(request):
    if request.method == 'POST':
        # handle payment or proof upload
        return redirect('order_success')
    return render(request, 'cart/cart_checkout.html')

def order_success(request):
    return render(request, 'cart/order_success.html') 

def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')  
