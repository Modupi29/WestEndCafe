from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from django.utils import timezone

def reservation(request):
    return render(request, 'booking/reservations.html')

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/booking_list.html', {'bookings': bookings})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'booking/booking_detail.html', {'booking': booking})

@login_required
def booking_create(request):
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')

        # Create and save the new booking
        Booking.objects.create(
            user=request.user,  # assign the logged-in user
            name=name,
            date=date,
            time=time,
            guests=guests
        )
        messages.success(request, "Booking created successfully!")
        return redirect('booking_list')

    return render(request, 'booking/booking_form.html', {'booking': None})


@login_required
def booking_edit(request, id):
    booking = get_object_or_404(Booking, id=id)
    if request.method == 'POST':
        booking.name = request.POST.get('customer_name')
        booking.date = request.POST.get('date')
        booking.time = request.POST.get('time')
        booking.guests = request.POST.get('guests')
        booking.save()
        messages.success(request, "Booking updated successfully!")
        return redirect('booking_list')
    return render(request, 'booking/booking_form.html', {'booking': booking})

@login_required
def booking_cancel(request, id):
    booking = get_object_or_404(Booking, id=id)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking canceled successfully!")
    return redirect('booking_list')

@login_required
def booking_complete(request, id):
    booking = get_object_or_404(Booking, id=id)
    if request.method == 'POST':
        booking.status = 'Completed'
        booking.save()
        messages.success(request, 'Booking marked as completed.')
        return redirect('booking_list')
    return render(request, 'booking/booking_complete.html', {'booking': booking}) 

@login_required
def booking_search(request):
    query = request.GET.get('q')
    bookings = Booking.objects.filter(user=request.user, name__icontains=query) if query else []
    return render(request, 'booking/booking_search.html', {'bookings': bookings, 'query': query})

@login_required
def upcoming_bookings(request):
    bookings = Booking.objects.filter(user=request.user, date__gte=timezone.now()).order_by('date')
    return render(request, 'booking/upcoming_bookings.html', {'bookings': bookings})

@login_required
def past_bookings(request):
    bookings = Booking.objects.filter(user=request.user, date__lt=timezone.now()).order_by('-date')
    return render(request, 'booking/past_bookings.html', {'bookings': bookings})

@login_required
def booking_reminder(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    # Logic to send reminder (e.g., email) would go here
    messages.info(request, f'Reminder sent for booking on {booking.date}.')
    return redirect('booking_list')
    return render(request, 'booking/booking_reminder.html', {'booking': booking})

@login_required
def booking_reschedule(request, pk): 
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking rescheduled successfully!')
            return redirect('booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking/booking_reschedule.html', {'form': form})

@login_required
def booking_user_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    return render(request, 'booking/booking_user_list.html', {'bookings': bookings})

@login_required
def booking_user_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'booking/booking_user_detail.html', {'booking': booking})

@login_required
def booking_user_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your booking has been updated.')
            return redirect('booking_user_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking/booking_user_edit.html', {'form': form})

@login_required
def booking_user_cancel(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.status = 'Cancelled'
        booking.save()
        messages.info(request, 'Your booking has been cancelled.')
        return redirect('booking_user_list')
    return render(request, 'booking/booking_user_cancel.html', {'booking': booking})

@login_required
def booking_user_complete(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.status = 'Completed'
        booking.save()
        messages.success(request, 'Your booking has been marked as completed.')
        return redirect('booking_user_list')
    return render(request, 'booking/booking_user_complete.html', {'booking': booking})

@login_required
def booking_user_reschedule(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your booking has been rescheduled.')
            return redirect('booking_user_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking/booking_user_reschedule.html', {'form': form})

@login_required
def booking_user_reminder(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    # Logic to send reminder (e.g., email) would go here
    messages.info(request, f'Reminder sent for your booking on {booking.date}.')
    return redirect('booking_user_list')
    return render(request, 'booking/booking_user_reminder.html', {'booking': booking})

@login_required
def booking_statistics(request):
    total_bookings = Booking.objects.filter(user=request.user).count()
    upcoming_count = Booking.objects.filter(user=request.user, date__gte=timezone.now()).count()
    past_count = Booking.objects.filter(user=request.user, date__lt=timezone.now()).count()
    cancelled_count = Booking.objects.filter(user=request.user, status='Cancelled').count()
    completed_count = Booking.objects.filter(user=request.user, status='Completed').count()

    stats = {
        'total_bookings': total_bookings,
        'upcoming_count': upcoming_count,
        'past_count': past_count,
        'cancelled_count': cancelled_count,
        'completed_count': completed_count,
    }
    return render(request, 'booking/booking_statistics.html', {'stats': stats})

@login_required
def booking_export(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    # Logic to export bookings (e.g., to CSV) would go here
    messages.success(request, 'Your bookings have been exported.')
    return redirect('booking_user_list')
    return render(request, 'booking/booking_export.html', {'bookings': bookings})

# Staff views for managing bookings

@staff_member_required
def manage_bookings(request):
    bookings = Booking.objects.all().order_by('-date')
    return render(request, 'booking/manage_bookings.html', {'bookings': bookings})

@staff_member_required
def manage_booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'booking/manage_booking_detail.html', {'booking': booking})

@staff_member_required
def manage_booking_toggle_status(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if booking.status == 'Cancelled':
        booking.status = 'Pending'
    else:
        booking.status = 'Cancelled'
    booking.save()
    messages.success(request, f"Booking status changed to {booking.status}.")
    return redirect('manage_bookings')

@staff_member_required
def manage_booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.info(request, "Booking deleted successfully.")
        return redirect('manage_bookings')
    return render(request, 'booking/manage_booking_delete.html', {'booking': booking})

@staff_member_required
def manage_booking_reschedule(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, 'Booking rescheduled successfully!')
            return redirect('manage_bookings')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking/manage_booking_reschedule.html', {'form': form})

@staff_member_required
def manage_booking_report(request):
    bookings = Booking.objects.all().order_by('-date')
    return render(request, 'booking/manage_booking_report.html', {'bookings': bookings})

@staff_member_required
def manage_booking_report_filter(request):
    bookings = Booking.objects.all().order_by('-date')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        bookings = bookings.filter(date__gte=start_date)
    if end_date:
        bookings = bookings.filter(date__lte=end_date)

    return render(request, 'booking/manage_booking_report.html', {'bookings': bookings, 'start_date': start_date, 'end_date': end_date})

@staff_member_required
def booking_report(request):
    bookings = Booking.objects.all().order_by('-date')
    return render(request, 'booking/booking_report.html', {'bookings': bookings})

@staff_member_required
def booking_report_filter(request):
    bookings = Booking.objects.all().order_by('-date')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        bookings = bookings.filter(date__gte=start_date)
    if end_date:
        bookings = bookings.filter(date__lte=end_date)

    return render(request, 'booking/booking_report.html', {'bookings': bookings, 'start_date': start_date, 'end_date': end_date})

@staff_member_required
def booking_statistics_admin(request):
    total_bookings = Booking.objects.count()
    upcoming_count = Booking.objects.filter(date__gte=timezone.now()).count()
    past_count = Booking.objects.filter(date__lt=timezone.now()).count()
    cancelled_count = Booking.objects.filter(status='Cancelled').count()
    completed_count = Booking.objects.filter(status='Completed').count()

    stats = {
        'total_bookings': total_bookings,
        'upcoming_count': upcoming_count,
        'past_count': past_count,
        'cancelled_count': cancelled_count,
        'completed_count': completed_count,
    }
    return render(request, 'booking/booking_statistics_admin.html', {'stats': stats})

@staff_member_required
def booking_export_admin(request):
    bookings = Booking.objects.all().order_by('-date')
    # Logic to export bookings (e.g., to CSV) would go here
    messages.success(request, 'Bookings have been exported.')
    return redirect('manage_bookings')
    return render(request, 'booking/booking_export.html', {'bookings': bookings})


