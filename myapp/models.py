from django.db import models
from datetime import datetime, timedelta
import random
from django.contrib.auth.models import User
class Visitor(models.Model):
    visitor_name = models.CharField(max_length=100)
    visitor_email = models.EmailField()
    category = models.CharField(max_length=50)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    designated_attendee = models.CharField(max_length=100)
    document = models.FileField(upload_to='visitor_documents/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.visitor_name

        
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username




class VisitorSchedule(models.Model):
    visitor = models.OneToOneField(Visitor, on_delete=models.CASCADE)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('Rescheduled', 'Rescheduled'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    rescheduled_date = models.DateField(blank=True, null=True)
    rescheduled_time = models.TimeField(blank=True, null=True)
    designated_attendee = models.CharField(max_length=100, blank=True, null=True)

    verification_code = models.CharField(max_length=4, blank=True, null=True)

    in_time = models.TimeField(blank=True, null=True)
    out_time = models.TimeField(blank=True, null=True)
    total_duration = models.DurationField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    def generate_verification_code(self):
        self.verification_code = str(random.randint(1000, 9999))
        self.save()

    def calculate_duration(self):
        if self.in_time and self.out_time:
            in_datetime = datetime.combine(datetime.today(), self.in_time)
            out_datetime = datetime.combine(datetime.today(), self.out_time)

            if out_datetime < in_datetime:
                out_datetime += timedelta(days=1)

            self.total_duration = out_datetime - in_datetime
            self.save()

    def get_total_duration_formatted(self):
        if self.total_duration:
            total_seconds = int(self.total_duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        return "0h 0m"

    def __str__(self):
        return f"{self.visitor.visitor_name} - {self.status}"
