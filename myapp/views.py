from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from datetime import datetime, timedelta
from .models import Visitor, VisitorSchedule
from django.core.paginator import Paginator


# HOME
def home(request):
    return render(request, 'home.html')


# DASHBOARD → default scheduled meets
def dashboard(request):
    return redirect('scheduled_meets')


# REGISTER VISITOR (no change needed)
def register_visitor(request):
    success = False

    if request.method == 'POST':
        visitor_name = request.POST.get('visitor_name')
        visitor_email = request.POST.get('visitor_email')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        document = request.FILES.get('document')
        designated_attendee = request.POST.get('designated_attendee')

        last_visitor = Visitor.objects.order_by('-id').first()
        next_visitor_id = last_visitor.id + 1 if last_visitor else 1


        try:
            appointment_date_obj = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            today = datetime.today().date()
            max_date = today + timedelta(days=10)

            if appointment_date_obj < today or appointment_date_obj > max_date:
                messages.error(request, 'Appointment date must be within 10 days.')
                return redirect('visitor_registration')

            appointment_time_obj = datetime.strptime(appointment_time, '%H:%M').time()
            if not (datetime.strptime('09:00', '%H:%M').time() <= appointment_time_obj <= datetime.strptime('18:00', '%H:%M').time()):
                messages.error(request, 'Appointment time must be between 09:00 AM and 06:00 PM.')
                return redirect('visitor_registration')

            while Visitor.objects.filter(visitor_id=next_visitor_id).exists():
                next_visitor_id += 1

            visitor = Visitor.objects.create(
                # visitor_id=next_visitor_id,
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


# ✅ GENERIC MEET VIEW (USE THIS EVERYWHERE)
def meets_by_status(request, status, template, title):
    schedules = VisitorSchedule.objects.filter(
        status__iexact=status
    ).select_related('visitor').order_by('-id')

    limit = request.GET.get('limit', 10)
    limit = int(limit) if str(limit).isdigit() else 10

    paginator = Paginator(schedules, limit)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, template, {
        'page_obj': page_obj,
        'limit': limit,
        'page_title': title
    })


# SPECIFIC PAGES
def scheduled_meets(request):
    return meets_by_status(
        request,
        status='Pending',
        template='scheduled_meets.html',
        title='Scheduled Meets'
    )


def approved_meets(request):
    return meets_by_status(
        request,
        status='Approved',
        template='approved_meets.html',
        title='Approved Meets'
    )


def rejected_meets(request):
    return meets_by_status(
        request,
        status='Rejected',
        template='rejected_meets.html',
        title='Rejected Meets'
    )


def rescheduled_meets(request):
    return meets_by_status(
        request,
        status='Rescheduled',
        template='rescheduled_meets.html',
        title='Rescheduled Meets'
    )


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
