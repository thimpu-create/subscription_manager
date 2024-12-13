from django.urls import path
from . import views
app_name = 'subscriptions'

urlpatterns = [
    path('', views.home, name = "home"),
    path('manage_subs/', views.manage_subs, name = "manage_subs"),
    path('get_reminders/', views.analys_report, name = "get_reminders"),
    path('analys_reports/', views.get_reminders, name = "analys_report"),
    path('add_subs/', views.add_subs_view, name = "add_subs_view"),
    path('record_payment/<int:subscription_id>/', views.record_payment, name='record_payment'),
    path('edit_subscription/<int:subscription_id>/', views.edit_subscription, name='edit_subscription'),
    path('delete_subscription/<int:subscription_id>/', views.deleted_subscription, name='delete_subscription'),
    path('payment_hsitory/<int:subscription_id>/', views.payment_history, name='payment_history'),
]