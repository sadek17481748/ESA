"""core_app/views.py — shared views used across the project."""
from django.shortcuts import render


def home(request):
    """Landing page — entry point for Heroku and local deploy."""
    return render(request, 'home.html')
