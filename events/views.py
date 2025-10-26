from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import Event
from .forms import EventForm

def event(request):
    events = Event.objects.filter(is_active=True).order_by('date', 'time')
    return render(request, 'events/event.html', {'events': events})

@login_required
def event_list(request):
    events = Event.objects.filter(is_active=True).order_by('date', 'time')
    return render(request, 'events/event_list.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, "Event created successfully!")
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_create.html', {'form': form})

@login_required
def event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_edit.html', {'form': form})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.info(request, "Event deleted successfully.")
        return redirect('event_list')
    return render(request, 'events/event_delete.html', {'event': event})
@login_required
def event_toggle_active(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.is_active = not event.is_active
    event.save()
    status = "activated" if event.is_active else "deactivated"
    messages.success(request, f"Event {status} successfully.")
    return redirect('event_list')

@login_required
def user_events(request):
    events = Event.objects.filter(created_by=request.user).order_by('-date', '-time')
    return render(request, 'events/user_events.html', {'events': events})

@login_required
def event_user_detail(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    return render(request, 'events/event_user_detail.html', {'event': event})

@login_required
def event_user_edit(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('user_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/event_user_edit.html', {'form': form})

@login_required
def event_user_delete(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    if request.method == 'POST':
        event.delete()
        messages.info(request, "Event deleted successfully.")
        return redirect('user_events')
    return render(request, 'events/event_user_delete.html', {'event': event})

@login_required
def event_user_toggle_active(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    event.is_active = not event.is_active
    event.save()
    status = "activated" if event.is_active else "deactivated"
    messages.success(request, f"Event {status} successfully.")
    return redirect('user_events')

def event_search(request):
    query = request.GET.get('q')
    events = Event.objects.filter(is_active=True)
    if query:
        events = events.filter(title__icontains=query) | events.filter(description__icontains=query)
    return render(request, 'events/event_search.html', {'events': events, 'query': query})

@login_required
def event_report(request):
    events = Event.objects.all().order_by('-date', '-time')
    return render(request, 'events/event_report.html', {'events': events})

@login_required
def event_report_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/event_report_detail.html', {'event': event})

@login_required
def event_report_filter(request):

    events = Event.objects.all().order_by('-date', '-time')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)

    return render(request, 'events/event_report.html', {'events': events, 'start_date': start_date, 'end_date': end_date})

@login_required
def event_upcoming(request):
    from django.utils import timezone
    events = Event.objects.filter(is_active=True, date__gte=timezone.now().date()).order_by('date', 'time')
    return render(request, 'events/event_upcoming.html', {'events': events})

@login_required
def event_past(request):
    from django.utils import timezone
    events = Event.objects.filter(date__lt=timezone.now().date()).order_by('-date', '-time')
    return render(request, 'events/event_past.html', {'events': events})

@login_required
def event_reminder(request, pk):
    event = get_object_or_404(Event, pk=pk, created_by=request.user)
    # Here you would implement the logic to send a reminder (e.g., email)
    messages.success(request, f"Reminder for event '{event.title}' has been sent.")
    return redirect('user_events')

# Staff views for managing events

@staff_member_required
def manage_events(request):
    events = Event.objects.all().order_by('-date', '-time')
    return render(request, 'events/manage_events.html', {'events': events})

@staff_member_required
def manage_event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/manage_event_detail.html', {'event': event})

@staff_member_required
def manage_event_toggle_active(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.is_active = not event.is_active
    event.save()
    status = "activated" if event.is_active else "deactivated"
    messages.success(request, f"Event {status} successfully.")
    return redirect('manage_events')

@staff_member_required
def manage_event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.info(request, "Event deleted successfully.")
        return redirect('manage_events')
    return render(request, 'events/manage_event_delete.html', {'event': event})

@staff_member_required
def manage_event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully!")
            return redirect('manage_events')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/manage_event_edit.html', {'form': form})

@staff_member_required
def manage_event_report(request):
    events = Event.objects.all().order_by('-date', '-time')
    return render(request, 'events/manage_event_report.html', {'events': events})

@staff_member_required
def manage_event_report_filter(request):

    events = Event.objects.all().order_by('-date', '-time')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date:
        events = events.filter(date__gte=start_date)
    if end_date:
        events = events.filter(date__lte=end_date)

    return render(request, 'events/manage_event_report.html', {'events': events, 'start_date': start_date, 'end_date': end_date})

@staff_member_required
def manage_event_report_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'events/manage_event_report_detail.html', {'event': event})

# End of recent edits
