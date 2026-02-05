from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from datetime import datetime, timedelta
from .models import Visitor, VisitorSchedule
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import RescheduleMeetForm


# HOME
def home(request):
    return render(request, 'home.html')


# DASHBOARD
def dashboard(request):
    return render(request, 'base_dashboard.html')


# REGISTER VISITOR
def register_visitor(request):
    success = False

    if request.method == 'POST':
        visitor_name = request.POST.get('visitor_name')
        visitor_email = request.POST.get('visitor_email')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        document = request.FILES.get('document')
        designated_attendee = request.POST.get('designated_attendee')

        try:
            appointment_date_obj = datetime.strptime(
                appointment_date, '%Y-%m-%d'
            ).date()

            today = datetime.today().date()
            max_date = today + timedelta(days=10)

            if appointment_date_obj < today or appointment_date_obj > max_date:
                messages.error(request, 'Appointment date must be within 10 days.')
                return redirect('visitor_registration')

            appointment_time_obj = datetime.strptime(
                appointment_time, '%H:%M'
            ).time()

            if not (
                datetime.strptime('09:00', '%H:%M').time()
                <= appointment_time_obj
                <= datetime.strptime('18:00', '%H:%M').time()
            ):
                messages.error(
                    request,
                    'Appointment time must be between 09:00 AM and 06:00 PM.'
                )
                return redirect('visitor_registration')

            visitor = Visitor.objects.create(
                visitor_name=visitor_name,
                visitor_email=visitor_email,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                document=document,
                category=request.POST.get('category'),
                reason=request.POST.get('reason'),
                designated_attendee=designated_attendee,
            )

            VisitorSchedule.objects.create(
                visitor=visitor,
                designated_attendee=designated_attendee,
                status='Pending'
            )

            success = True

        except ValueError:
            messages.error(request, 'Invalid date or time format.')

    return render(request, 'home.html', {'success': success})


# SCHEDULED MEETS
def scheduled_meets(request):
    limit = request.GET.get('limit', 5)
    q = request.GET.get('q', '')

    schedules = VisitorSchedule.objects.filter(status='Pending')

    if q:
        schedules = schedules.filter(
            Q(visitor__visitor_name__icontains=q) |
            Q(visitor__id__icontains=q)
        )

    paginator = Paginator(schedules, limit)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'scheduled_meets.html', {
        'page_obj': page_obj,
        'limit': limit,
    })


# APPROVED MEETS
def approved_meets(request):
    limit = request.GET.get('limit', 5)
    q = request.GET.get('q', '')

    schedules = VisitorSchedule.objects.filter(status='Approved')

    if q:
        schedules = schedules.filter(
            Q(visitor__visitor_name__icontains=q) |
            Q(visitor__id__icontains=q)
        )

    paginator = Paginator(schedules, limit)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'approved_meets.html', {
        'page_obj': page_obj,
        'limit': limit,
    })


# REJECTED MEETS
def rejected_meets(request):
    limit = request.GET.get('limit', 5)
    q = request.GET.get('q', '')

    schedules = VisitorSchedule.objects.filter(status='Rejected')

    if q:
        schedules = schedules.filter(
            Q(visitor__visitor_name__icontains=q) |
            Q(visitor__id__icontains=q)
        )

    paginator = Paginator(schedules, limit)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'rejected_meets.html', {
        'page_obj': page_obj,
        'limit': limit,
    })


# RESCHEDULED MEETS
def rescheduled_meets(request):
    limit = request.GET.get('limit', 5)
    q = request.GET.get('q', '')

    schedules = VisitorSchedule.objects.filter(status='Rescheduled')

    if q:
        schedules = schedules.filter(
            Q(visitor__visitor_name__icontains=q) |
            Q(visitor__id__icontains=q)
        )

    paginator = Paginator(schedules, limit)
    page_obj = paginator.get_page(request.GET.get('page'))

    return render(request, 'rescheduled_meets.html', {
        'page_obj': page_obj,
        'limit': limit,
    })


# RESCHEDULE MEET (FIXED – SINGLE VERSION ONLY)
def reschedule_meet(request, pk):
    schedule = get_object_or_404(VisitorSchedule, id=pk)
    visitor = schedule.visitor

    if request.method == "POST":
        visitor.appointment_date = request.POST.get("appointment_date")
        visitor.appointment_time = request.POST.get("appointment_time")
        visitor.save()

        schedule.status = "Rescheduled"
        schedule.save()

        messages.success(request, "Meeting rescheduled successfully.")
        return redirect("rescheduled_meets")

    return render(request, "reschedule_form.html", {
        "schedule": schedule
    })


# UPDATE STATUS
def update_schedule_status(request, schedule_id, new_status):
    schedule = get_object_or_404(VisitorSchedule, id=schedule_id)
    schedule.status = new_status.capitalize()
    schedule.save()
    return redirect(f'{new_status.lower()}_meets')


# LOGOUT
def user_logout(request):
    logout(request)
    return redirect('login')

def delete_meet(request, schedule_id):
    schedule = get_object_or_404(VisitorSchedule, id=schedule_id)

    if request.method == "POST":
        schedule.delete()
        messages.success(request, "Meeting deleted successfully")
        return redirect(request.POST.get("next", "dashboard"))

    return render(request, "confirm_delete.html", {
        "schedule": schedule
    })