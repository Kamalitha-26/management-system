from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import Visitor
from django.conf import settings
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def visitor_registration(request):
    success = False  # Flag to show success notification

    if request.method == 'POST':
        # Get form data
        visitor_name = request.POST.get('visitor_name')
        visitor_email = request.POST.get('visitor_email')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        document = request.FILES.get('document')
        designated_attendee = request.POST.get('designated_attendee')

        # Ensure unique visitor ID
        last_visitor = Visitor.objects.order_by('-visitor_id').first()
        next_visitor_id = last_visitor.visitor_id + 1 if last_visitor else 101

        try:
            # Validate appointment date
            appointment_date_obj = datetime.strptime(appointment_date, '%Y-%m-%d').date()
            today = datetime.today().date()
            max_date = today + timedelta(days=10)

            if appointment_date_obj < today or appointment_date_obj > max_date:
                messages.error(request, 'Appointment date must be between today and the next 10 days.')
                return redirect('visitor_registration')

            # Validate appointment time
            appointment_time_obj = datetime.strptime(appointment_time, '%H:%M').time()
            if appointment_time_obj < datetime.strptime('09:00', '%H:%M').time() or appointment_time_obj > datetime.strptime('18:00', '%H:%M').time():
                messages.error(request, 'Appointment time must be between 09:00 AM and 06:00 PM.')
                return redirect('visitor_registration')

            # Send email to the designated attendee
            attendee_email_mapping = {
                'Member 1': 'athithyag24@gmail.com',
                'Member 2': 'athithyag24@gmail.com',
                'General': 'athithyag24@gmail.com',
            }
            attendee_email = attendee_email_mapping.get(designated_attendee)

            if attendee_email:
                try:
                    attendee_subject = f'New Visitor Scheduled - {visitor_name}'
                    attendee_message = f"""
Dear Team,

A new visitor Appointment has been scheduled. Below are the details of the visitor's appointment:

Visitor Name: {visitor_name}
Appointment Date: {appointment_date}
Appointment Time: {appointment_time}
Reason: {request.POST.get('reason')}

Please ensure all necessary arrangements are made to facilitate the visitor's appointment.

Best Regards,
Pinesphere Solutions
"""
                    send_mail(
                        attendee_subject,
                        attendee_message,
                        settings.EMAIL_HOST_USER,
                        [attendee_email],
                        fail_silently=False,
                    )
                except Exception as e:
                    print(f"Error sending email to attendee: {e}")
                    messages.error(request, 'There was an issue notifying the designated attendee.')

            # Ensure unique visitor ID
            while Visitor.objects.filter(visitor_id=next_visitor_id).exists():
                next_visitor_id += 1

            # Save visitor data to the database
            new_visitor = Visitor(
                visitor_id=next_visitor_id,
                visitor_name=visitor_name,
                visitor_email=visitor_email,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                document=document,
                category=request.POST.get('category'),
                reason=request.POST.get('reason'),
                designated_attendee=designated_attendee,
            )
            new_visitor.save()

            # Email content for visitor
            email_subject = 'Visitor Registration Successful - Pinesphere Solutions'
            email_message = f"""
Dear {visitor_name},

Thank you for registering as a visitor with Pinesphere Solutions. Below are the details of your scheduled appointment:

Your appointment has been successfully scheduled as follows:

Appointment Date: {appointment_date}
Appointment Time: {appointment_time}

If you need to reschedule your appointment, please click the link below:
Reschedule Your Appointment: http://127.0.0.1:8000/reschedule-meet/{new_visitor.id}/

We look forward to welcoming you to our office.

Best Regards,
Pinesphere Solutions
"""

            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [visitor_email],
                fail_silently=False,
            )

            # Create a corresponding VisitorSchedule object
            VisitorSchedule.objects.create(visitor=new_visitor, designated_attendee=designated_attendee)

            success = True
            # messages.success(request, 'Visitor registration successful!')

        except ValueError:
            messages.error(request, 'Invalid date or time format.')
            return redirect('visitor_registration')

    return render(request, 'home.html', {'success': success})