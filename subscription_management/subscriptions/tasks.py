from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from datetime import timedelta
from .models import Subscription

@shared_task
def send_subscription_reminders():
    today = now().date()
    reminder_window = [today, today + timedelta(days=1)]  # Today or tomorrow
    subscriptions = Subscription.objects.filter(next_due_date__in=reminder_window)
    
    for subscription in subscriptions:
        try:
            subject = f"Reminder: {subscription.name} Subscription Due"
            message = (
                f"Hello {subscription.user.first_name},\n\n"
                f"This is a reminder that your subscription for {subscription.name} is due "
                f"on {subscription.next_due_date}. Please ensure timely renewal to avoid interruption.\n\n"
                "Thank you!"
            )
            send_mail(
                subject,
                message,
                'thimpu@adventurecode.io',  # Replace with your "from" email
                [subscription.user.email],
                fail_silently=False,  # Raise errors for debugging
            )
        except Exception as e:
            # Log the error (use logging module in production)
            print(f"Failed to send reminder for {subscription.name}: {e}")
