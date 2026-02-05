from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # DASHBOARD (front page) - Use only one
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # VISITOR REGISTRATION
    path('register/', views.register_visitor, name='visitor_registration'),

    # MEETS PAGES
    path('meets/scheduled/', views.scheduled_meets, name='scheduled_meets'),
    path('meets/approved/', views.approved_meets, name='approved_meets'),
    path('meets/rejected/', views.rejected_meets, name='rejected_meets'),
    path('meets/rescheduled/', views.rescheduled_meets, name='rescheduled_meets'),

    # UPDATE STATUS
    path(
        'meets/update/<int:schedule_id>/<str:new_status>/',
        views.update_schedule_status,
        name='update_schedule_status'
    ),

    # LOGOUT
    path('logout/', views.user_logout, name='logout'),

    path(
        'reschedule/<int:schedule_id>/',
        views.reschedule_meet,
        name='reschedule_meet'
    ),
    

    # urls.py
    path('meets/reschedule/<int:pk>/', views.reschedule_meet, name='reschedule_meet'),
    path('meets/rescheduled/', views.rescheduled_meets, name='rescheduled_meets'),

    path('meets/delete/<int:schedule_id>/', views.delete_meet, name='delete_meet'),

]