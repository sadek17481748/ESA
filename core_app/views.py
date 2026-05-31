"""core_app/views.py — shared views used across the project."""
from django.shortcuts import render

from .home_leaderboards import get_schools_of_the_week, get_students_of_the_week


def home(request):
    """Landing page — entry point for Heroku and local deploy."""
    context = {}
    if not request.user.is_authenticated:
        context['students_of_week'] = get_students_of_the_week()
        context['schools_of_week'] = get_schools_of_the_week()
    return render(request, 'home.html', context)
