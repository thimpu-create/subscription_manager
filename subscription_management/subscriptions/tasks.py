from celery import shared_task
from django.core.mail import send_mail
from datetime import datetime, timedelta
from .models import Subscription

@shared_task
def send_subscription_reminders():
    today = datetime.now().date()
    subscriptions = Subscription.objects.filter(next_due_date__in=[today, today + timedelta(days=1)])
    for subscription in subscriptions:
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
            [subscription.user.email],  # Send to the user's email
        )
