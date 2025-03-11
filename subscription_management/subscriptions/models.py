from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    SERVICE_CATEGORIES = [
        ('entertainment', 'Entertainment'),
        ('utility', 'Utility'),
        ('software', 'Software'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=SERVICE_CATEGORIES, default='other')
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_date = models.DateField()
    renewal_frequency = models.CharField(max_length=10, choices=[
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ])
    next_due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Calculate the next due date if it's not manually provided
        if not self.next_due_date or self.next_due_date == now().date():
            if self.renewal_frequency == 'monthly':
                self.next_due_date = self.subscription_date + timedelta(days=30)
            elif self.renewal_frequency == 'yearly':
                self.next_due_date = self.subscription_date + timedelta(days=365)
        super().save(*args, **kwargs)


class Paid_subscription(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    paid_date = models.DateField()