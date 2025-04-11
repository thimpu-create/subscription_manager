from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from .models import SMTPSettings
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@login_required
def settings_page(request):
    print("settigns loaded")
    active_page = "settings"
    try:
        smtp = SMTPSettings.objects.get(user=request.user.id)
    except SMTPSettings.DoesNotExist:
        smtp = None
    context = {
        'smtp_settings': smtp,
        'active_page': active_page
    }
    return render(request, 'settings.html', context)


@login_required
@csrf_exempt  # Only use this if you're not sending CSRF token in JS
def email_config_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            host = data.get('host')
            port = data.get('port')
            password = data.get('password')
            security = data.get('encryption')

            ssl_bool = security == 'ssl'
            tls_bool = security == 'tls'

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

            if not created:
                smtp_settings.email = email
                smtp_settings.host = host
                smtp_settings.port = port
                smtp_settings.password = password
                smtp_settings.use_ssl = ssl_bool
                smtp_settings.use_tls = tls_bool
                smtp_settings.save()

            return JsonResponse({'success': True, 'message': 'SMTP settings saved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)