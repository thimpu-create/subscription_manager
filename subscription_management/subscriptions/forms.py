from django import forms
from datetime import timedelta
from .models import *

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        exclude = ['user', 'next_due_date']  # Exclude both user and next_due_date

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Calculate next_due_date based on subscription_date and renewal_frequency
        if instance.renewal_frequency == 'monthly':
            instance.next_due_date = instance.subscription_date + timedelta(days=30)
        elif instance.renewal_frequency == 'yearly':
            instance.next_due_date = instance.subscription_date + timedelta(days=365)
        else:
            instance.next_due_date = instance.subscription_date

        if commit:
            instance.save()
        return instance
