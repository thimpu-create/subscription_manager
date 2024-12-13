# Django Subscription Management System

A simple subscription management system built with Django, designed to track your subscriptions, mark them as paid, and manage due dates efficiently.

## Features

- **Add Subscription**: Add a new subscription with details like name, category, cost, and renewal frequency.
- **View Subscriptions**: View a list of your subscriptions with next due dates and renewal frequencies.
- **Payment History**: Track payments made for each subscription with dates.
- **Mark as Paid**: Mark a subscription as paid, which updates its payment history and next due date.
- **Filter Subscriptions**: View subscriptions based on their category and payment status.
- **Responsive Design**: The application is mobile-friendly with an adaptive layout for desktop and mobile views.

## Technologies Used

- **Python 3.x** - Programming language
- **Django** - Web framework for building the application
- **SQLite** - Default database for local development (can be replaced with PostgreSQL or MySQL)
- **Bootstrap 5** - For styling the front-end

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/django-subscription-management.git

2. Navigate to the project directory:

   ```bash
   cd django-subscription-management
   
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt

4. Apply migrations to set up the database:

   ```bash
   python manage.py migrate
   
5. Create a superuser to access the Django admin:

    ```bash
    python manage.py createsuperuser
    
6. Run the development server:

    ```bash
    python manage.py runserver
    
7. Open your browser and visit http://127.0.0.1:8000/ to use the application.

## Usage
- **Add Subscription**: Navigate to the "Add Subscription" page to create a new subscription with details like name, cost, and renewal frequency.
- **Mark Subscription as Paid**: Once a subscription is added, you can mark it as paid by clicking the "Mark as Paid" button on the subscription list page.
- **View Payment History**: Click on a subscription to see the payment history for that specific subscription.
- **Manage Subscriptions**: Edit or delete subscriptions as needed from the subscription list.
