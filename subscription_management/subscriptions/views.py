from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from .forms import *
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from datetime import datetime, timedelta
import json

# Create your views here.

@login_required
def home(request):
    return render(request, 'home.html')

@login_required

def manage_subs(request):
    subscriptions = Subscription.objects.filter(user=request.user).order_by('next_due_date')  # Order by the next due date, descending
    return render(request, 'manage_subscription.html', {'subscriptions': subscriptions})
@login_required

def get_reminders(request):
    return render(request, 'get_reminders.html')
@login_required

def analys_report(request):
    try:
        # Get user's subscriptions
        subscriptions = Subscription.objects.filter(user=request.user)
        
        # Calculate total costs
        monthly_subs = subscriptions.filter(renewal_frequency='monthly')
        yearly_subs = subscriptions.filter(renewal_frequency='yearly')
        
        total_monthly_cost = sum([sub.cost for sub in monthly_subs])
        total_yearly_subs_cost = sum([sub.cost for sub in yearly_subs])
        
        total_yearly_cost = (total_monthly_cost * 12) + total_yearly_subs_cost
        
        # Category distribution with proper labels
        categories = []
        category_costs = []
        category_map = dict(Subscription.SERVICE_CATEGORIES)
        
        for category, label in Subscription.SERVICE_CATEGORIES:
            cost = sum([sub.cost for sub in subscriptions.filter(category=category)])
            if cost > 0:
                categories.append(label)  # Use display name instead of code
                category_costs.append(float(cost))
        
        # Get monthly trend
        months = []
        monthly_costs = []
        today = datetime.now()
        
        for i in range(6):
            date = today - timedelta(days=30*i)
            month = date.strftime('%B')
            months.insert(0, month)
            
            month_payments = Paid_subscription.objects.filter(
                subscription__user=request.user,
                paid_date__year=date.year,
                paid_date__month=date.month
            ).select_related('subscription')
            
            month_cost = sum([payment.subscription.cost for payment in month_payments])
            monthly_costs.insert(0, float(month_cost))
        
        context = {
            'subscriptions': subscriptions,
            'total_monthly_cost': round(total_monthly_cost, 2),
            'total_yearly_cost': round(total_yearly_cost, 2),
            'total_subscriptions': subscriptions.count(),
            'upcoming_renewals': subscriptions.filter(
                next_due_date__lte=datetime.now().date() + timedelta(days=7)
            ).count(),
            'categories': json.dumps(categories),
            'category_costs': json.dumps(category_costs),
            'months': json.dumps(months),
            'monthly_costs': json.dumps(monthly_costs),
        }
        
        return render(request, 'analys_reports.html', context)
    except Exception as e:
        print(f"Error in analytics: {str(e)}")  # For debugging
        return render(request, 'analys_reports.html', {
            'error': 'Unable to load analytics data',
            'subscriptions': Subscription.objects.filter(user=request.user)
        })

@login_required

def add_subs_view(request):
    if request.method == "GET":
        form = SubscriptionForm(user=request.user)
        return render(request, 'add_subs.html', {'form': form})
    if request.method == "POST":
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect('subscriptions:manage_subs')

@login_required

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

@login_required

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
@login_required
def deleted_subscription(request, subscription_id):
    # Fetch the subscription object by its ID, or return 404 if not found
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    # Delete the subscription from the database
    subscription.delete()

    # Optionally, redirect to the subscriptions management page or another page
    return redirect('subscriptions:manage_subs')  # Adjust the URL name to match your view

@login_required
def payment_history(request, subscription_id):
    # Fetch the subscription by its ID
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    # Retrieve the payment history for the given subscription
    payment_history = Paid_subscription.objects.filter(subscription=subscription).order_by('-paid_date')

    # Pass the subscription and payment history to the template
    return render(request, 'payment_history.html', {'subscription': subscription, 'payment_history': payment_history})



def login_form(request):
    return render(request, 'login_form.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('subscriptions:home')
        return redirect('subscriptions:login_form')
    
def logout_view(request):
    logout(request)
    return redirect('subscriptions:login_form')