from django.urls import path
from . import views

urlpatterns = [

    # HOME & DASHBOARD
    path('', views.home, name='home'),
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
]
