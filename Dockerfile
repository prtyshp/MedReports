# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code into the container at /app
COPY . /app/

# Run database migrations
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Define environment variable for Django
ENV DJANGO_SETTINGS_MODULE=medlgl.settings

# Railway sets the PORT environment variable to the port that the service is exposed on.
# Your application should use this environment variable to listen on this port.
# For example, you can modify the CMD to use the PORT environment variable as follows:

CMD gunicorn medlgl.wsgi:application --bind 0.0.0.0:$PORT
