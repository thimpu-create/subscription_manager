from django.urls import path
from . import views
app_name = 'settings'

urlpatterns = [
    path('', views.settings_page, name='settings_page'),
    path('email_config_view/', views.email_config_view, name='email_config_view'),
]