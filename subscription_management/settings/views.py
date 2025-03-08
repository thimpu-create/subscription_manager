from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import SMTPSettings
# Create your views here.

@login_required
def settings_page(request):
    print("settigns loaded")
    try:
        smtp = SMTPSettings.objects.get(user=request.user.id)
    except SMTPSettings.DoesNotExist:
        smtp = None
    context = {
        'smtp_settings': smtp
    }
    return render(request, 'settings.html', context)


@login_required
def email_config_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        host = request.POST.get('host')
        port = request.POST.get('port')
        password = request.POST.get('password')
        security = request.POST.get('security')

        ssl_bool = False
        tls_bool = False

        if security == 'ssl':
            ssl_bool = True
        if security == 'tls':
            tls_bool = True
        # Get or create SMTP settings for the user
        smtp_settings, created = SMTPSettings.objects.get_or_create(
            user=request.user,
            defaults={
                'email': email,
                'host': host,
                'port': port,
                'password': password,
                'use_ssl': ssl_bool,
                'use_tls': tls_bool
            }
        )

        # If settings already existed, update them
        if not created:
            smtp_settings.email = email
            smtp_settings.host = host
            smtp_settings.port = port
            smtp_settings.password = password
            smtp_settings.use_ssl = ssl_bool
            smtp_settings.use_tls = tls_bool
            smtp_settings.save()
        
        return redirect('settings:settings_page')