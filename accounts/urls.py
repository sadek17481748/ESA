from django.urls import path

from .views import MeView, RegisterView, UserListView

app_name = 'accounts'

urlpatterns = [
    path('me/', MeView.as_view(), name='me'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user_list'),
]
