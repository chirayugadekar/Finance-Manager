# login_app/urls.py

from django.urls import path
from .views import login_view

urlpatterns = [
    path('', login_view, name='login'),  # This handles http://127.0.0.1:8000/
]
