from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.http.response import HttpResponse
# Create your views here.


def home(request):
    return render(request, 'home.html')


def manage_subs(request):
    subscriptions = Subscription.objects.all().order_by('next_due_date')  # Order by the next due date, descending
    return render(request, 'manage_subscription.html', {'subscriptions': subscriptions})

def get_reminders(request):
    return render(request, 'get_reminders.html')

def analys_report(request):
    return render(request, 'analys_reports.html')


def add_subs_view(request):
    if request.method == "GET":
        form = SubscriptionForm()
        return render(request, 'add_subs.html', {'form': form})
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('subscriptions:manage_subs')


def record_payment(request, subscription_id):
    # Fetch the subscription object by its ID
    subscription = Subscription.objects.get(id=subscription_id)

    # Record the payment in Paid_subscription (this stores payment history)
    payment = Paid_subscription.objects.create(
        subscription=subscription,
        paid_date=timezone.now()  # Use the current date for paid_date
    )

    # Logic to calculate the next due date based on the renewal frequency
    if subscription.renewal_frequency == 'monthly':
        # Add 1 month to the current next_due_date
        next_due_date = subscription.next_due_date + timedelta(days=30)
    elif subscription.renewal_frequency == 'yearly':
        # Add 1 year to the current next_due_date
        next_due_date = subscription.next_due_date + timedelta(days=365)
    else:
        # If there's another frequency, handle accordingly or leave unchanged
        next_due_date = subscription.next_due_date  # Default, no change

    # Update the subscription with the new next_due_date
    subscription.next_due_date = next_due_date
    subscription.save()

    return redirect('subscriptions:manage_subs')  # Redirect to the subscriptions management page


def edit_subscription(request, subscription_id):
    # Retrieve the subscription object by its ID
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    if request.method == 'POST':
        # If the form is submitted (POST request), bind the data to the form
        form = SubscriptionForm(request.POST, instance=subscription)
        
        if form.is_valid():
            # If the form is valid, save the changes to the subscription
            form.save()
            # Redirect to the subscriptions management page or wherever appropriate
            return redirect('subscriptions:manage_subs')
    else:
        # If the form is not submitted, create a form instance with the current subscription data
        form = SubscriptionForm(instance=subscription)

    # Render the form in the template
    return render(request, 'edit_subs.html', {'form': form})

def deleted_subscription(request, subscription_id):
    # Fetch the subscription object by its ID, or return 404 if not found
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    # Delete the subscription from the database
    subscription.delete()

    # Optionally, redirect to the subscriptions management page or another page
    return redirect('subscriptions:manage_subs')  # Adjust the URL name to match your view


def payment_history(request, subscription_id):
    # Fetch the subscription by its ID
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    # Retrieve the payment history for the given subscription
    payment_history = Paid_subscription.objects.filter(subscription=subscription).order_by('-paid_date')

    # Pass the subscription and payment history to the template
    return render(request, 'payment_history.html', {'subscription': subscription, 'payment_history': payment_history})