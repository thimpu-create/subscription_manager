# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

# Copy the entire project (including manage.py) to the container
COPY . /app/

# Run migrations
RUN python3 manage.py migrate

# Create superuser (non-interactively)
RUN python3 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'password')"

# # Collect static files (optional)
# RUN python3 manage.py collectstatic --noinput

# Expose the application port
EXPOSE 8000

# Set environment variables for Django settings (optional)
ENV DJANGO_SETTINGS_MODULE=subscription_management.settings

# Start the application using the built-in Python server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
