# reports/urls.py

from django.urls import path
from .views import download_pdf, home, injury_report  # Import the required view functions

urlpatterns = [
    path('', home, name='home'),
    path('injury_report/', injury_report, name='injury_report'),  # Add the path for the injury report
    path('download_pdf/', download_pdf, name='download_pdf'),

    # ... other URL patterns ...
]