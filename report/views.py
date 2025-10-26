from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from order.models import Order, OrderItem
from booking.models import Booking
from review.models import Review
from .forms import ReportFilterForm

@staff_member_required
def report_list(request):
    return render(request, 'report/report_list.html')

@staff_member_required
def report_create(request):
    # Placeholder for report creation logic
    return render(request, 'report/report_create.html') 

@staff_member_required
def report_edit(request, pk):
    # Placeholder for report editing logic
    return render(request, 'report/report_edit.html', {'pk': pk})
@staff_member_required
def report_delete(request, pk):
    # Placeholder for report deletion logic
    return render(request, 'report/report_delete.html', {'pk': pk})

@staff_member_required
def report_detail(request, pk):
    # Placeholder for report detail logic
    return render(request, 'report/report_detail.html', {'pk': pk})


@staff_member_required
def dashboard(request):
    return render(request, 'report/report_dashboard.html')

@staff_member_required
def report_orders(request):
    orders = Order.objects.all().order_by('-date_created')
    total_sales = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_orders = orders.count()
    
    if request.method == 'POST':
        form = ReportFilterForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            orders = orders.filter(date_created__date__gte=start, date_created__date__lte=end)
            total_sales = orders.aggregate(Sum('total_price'))['total_price__sum'] or 0
            total_orders = orders.count()
    else:
        form = ReportFilterForm()

    return render(request, 'report/report_orders.html', {
        'orders': orders,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'form': form
    })

@staff_member_required
def report_bookings(request):
    bookings = Booking.objects.all().order_by('-date')
    total_bookings = bookings.count()
    
    if request.method == 'POST':
        form = ReportFilterForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            bookings = bookings.filter(date__gte=start, date__lte=end)
            total_bookings = bookings.count()
    else:
        form = ReportFilterForm()

    return render(request, 'report/report_bookings.html', {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'form': form
    })

@staff_member_required
def report_reviews(request):
    reviews = Review.objects.all().order_by('-date_created')
    average_rating = reviews.aggregate(Sum('rating'))['rating__sum'] or 0
    total_reviews = reviews.count()
    avg_rating = round(average_rating / total_reviews, 2) if total_reviews > 0 else 0

    if request.method == 'POST':
        form = ReportFilterForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            reviews = reviews.filter(date_created__date__gte=start, date_created__date__lte=end)
            total_reviews = reviews.count()
            average_rating = reviews.aggregate(Sum('rating'))['rating__sum'] or 0
            avg_rating = round(average_rating / total_reviews, 2) if total_reviews > 0 else 0
    else:
        form = ReportFilterForm()

    return render(request, 'report/report_reviews.html', {
        'reviews': reviews,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating,
        'form': form
    })

@staff_member_required
def report_order_items(request):
    order_items = OrderItem.objects.values('menu_item__name').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_quantity')

    if request.method == 'POST':
        form = ReportFilterForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start_date']
            end = form.cleaned_data['end_date']
            order_items = OrderItem.objects.filter(
                order__date_created__date__gte=start,
                order__date_created__date__lte=end
            ).values('menu_item__name').annotate(
                total_quantity=Sum('quantity'),
                total_revenue=Sum('price')
            ).order_by('-total_quantity')
    else:
        form = ReportFilterForm()

    return render(request, 'report/report_order_items.html', {
        'order_items': order_items,
        'form': form
    })

@staff_member_required
def report_summary(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_bookings = Booking.objects.count()
    total_reviews = Review.objects.count()
    average_rating = Review.objects.aggregate(Sum('rating'))['rating__sum'] or 0
    avg_rating = round(average_rating / total_reviews, 2) if total_reviews > 0 else 0

    return render(request, 'report/report_summary.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_bookings': total_bookings,
        'total_reviews': total_reviews,
        'avg_rating': avg_rating
    })
