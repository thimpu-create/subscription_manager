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

# Expose the application port
EXPOSE 8000

# Set environment variables for Django settings (optional)
ENV DJANGO_SETTINGS_MODULE=my_project.settings

# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "my_project.wsgi:application"]
