from django import forms
from .models import Profile, Visitor, VisitorSchedule


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role']


class VisitorForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = [
            'visitor_name',
            'visitor_email',
            'category',
            'appointment_date',
            'appointment_time',
            'reason',
            'designated_attendee',
            'document'
        ]


# ✅ THIS IS THE FIX
class RescheduleMeetForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['appointment_date', 'appointment_time']
        widgets = {
            'appointment_date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'appointment_time': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
        }
