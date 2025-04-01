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
        is_new = self.pk is None
        # Calculate the next due date if it's not manually provided
        if not self.next_due_date or self.next_due_date == now().date():
            if self.renewal_frequency == 'monthly':
                self.next_due_date = self.subscription_date + timedelta(days=30)
            elif self.renewal_frequency == 'yearly':
                self.next_due_date = self.subscription_date + timedelta(days=365)
        super().save(*args, **kwargs)
        
        if is_new:
            SubscriptionActivity.log_activity(
                self,
                'created',
                f'Subscription created for {self.name}',
                self.cost
            )

    def get_recent_activities(self, limit=10):
        return self.activities.all()[:limit]

class Paid_subscription(models.Model):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    paid_date = models.DateField()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SubscriptionActivity.log_activity(
            self.subscription,
            'paid',
            f'Payment made for {self.subscription.name}',
            self.subscription.cost
        )

class SubscriptionActivity(models.Model):
    ACTIVITY_TYPES = [
        ('created', 'Subscription Created'),
        ('renewed', 'Subscription Renewed'),
        ('paid', 'Payment Made'),
        ('modified', 'Subscription Modified'),
    ]
    
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def log_activity(cls, subscription, activity_type, description, amount=None):
        return cls.objects.create(
            subscription=subscription,
            activity_type=activity_type,
            description=description,
            amount=amount
        )