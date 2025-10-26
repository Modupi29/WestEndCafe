from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.cart import Cart
from cart.models import Order  # Make sure this is your Order model

def order_list(request):
    # Get all orders for the currently logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-order_date')

    context = {
        'orders': orders,
    }
    return render(request, 'order/order_list.html', context)

@login_required
def order_form(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/order_form.html', {'order': order})

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('menu_list')

    if request.method == 'POST':
        form = CheckoutForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    item=item['item'],
                    quantity=item['quantity']
                )
            cart.clear()
            messages.success(request, "Order placed successfully!")
            return redirect('order_success', order_id=order.id)
    else:
        form = CheckoutForm()

    return render(request, 'order/checkout.html', {'cart': cart, 'form': form})

@login_required
def order_list(request):
    # Get all orders for the currently logged-in user
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders,
    }
    return render(request, 'order/order_list.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order/order_detail.html', {
        'order': order,
        'order_items': order_items
    })

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order/order_success.html', {'order': order})

@login_required
def order_delete(request, order_id):
    if request.method == "POST":
        try:
            order = Order.objects.get(id=order_id, user=request.user)
            order.delete()
            return JsonResponse({'success': True, 'message': 'Order deleted successfully.'})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Order not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

@login_required
def order_complete(request, order_id):  
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'Delivered':
        order.status = 'Completed'
        order.save()
        messages.success(request, "Order marked as completed.")
    else:
        messages.error(request, "Order cannot be marked as completed at this stage.")
    return redirect('order_list')

@login_required
def order_proof_upload(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        form = CheckoutForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, "Proof of payment uploaded successfully.")
            return redirect('order_detail', order_id=order.id)
    else:
        form = CheckoutForm(instance=order)
    return render(request, 'order/order_proof_upload.html', {'form': form, 'order': order})

# Staff views for managing orders
from django.contrib.admin.views.decorators import staff_member_required 
@staff_member_required
def manage_orders(request):
    orders = Order.objects.all().order_by('-date_created')
    return render(request, 'order/manage_orders.html', {'orders': orders})

@staff_member_required
def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)
    if status in dict(Order.STATUS_CHOICES).keys():
        order.status = status
        order.save()
        messages.success(request, f"Order status updated to {status}.")
    else:
        messages.error(request, "Invalid status.")
    return redirect('manage_orders')

@staff_member_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        messages.success(request, "Order deleted successfully.")
        return redirect('manage_orders')
    return render(request, 'order/delete_order.html', {'order': order}) 
 
@staff_member_required
def order_report(request):
    from django.db.models import Count, Sum
    from django.utils.timezone import now, timedelta

    last_month = now() - timedelta(days=30)
    orders = Order.objects.filter(date_created__gte=last_month)
    total_orders = orders.count()
    total_revenue = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    status_counts = orders.values('status').annotate(count=Count('status'))

    return render(request, 'order/order_report.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'status_counts': status_counts,
        'orders': orders,
    })

@staff_member_required
def order_detail_admin(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)
    return render(request, 'order/order_detail_admin.html', {'order': order, 'order_items': order_items})

@staff_member_required
def search_orders(request):
    query = request.GET.get('q', '')
    orders = Order.objects.filter(id__icontains=query) | Order.objects.filter(user__username__icontains=query)
    return render(request, 'order/search_orders.html', {'orders': orders, 'query': query})

@staff_member_required
def filter_orders_by_status(request, status):
    orders = Order.objects.filter(status=status)
    return render(request, 'order/filter_orders.html', {'orders': orders, 'status': status})

@staff_member_required
def filter_orders_by_date(request):
    from django.utils.timezone import now, timedelta
    days = int(request.GET.get('days', 7))
    start_date = now() - timedelta(days=days)
    orders = Order.objects.filter(date_created__gte=start_date)
    return render(request, 'order/filter_orders.html', {'orders': orders, 'days': days})

@staff_member_required
def export_orders_csv(request):
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'

    writer = csv.writer(response)
    writer.writerow(['Order ID', 'User', 'Total Price', 'Status', 'Date Created'])

    orders = Order.objects.all().order_by('-date_created')
    for order in orders:
        writer.writerow([order.id, order.user.username, order.total_price, order.status, order.date_created])

    return response