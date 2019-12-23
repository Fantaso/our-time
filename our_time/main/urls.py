from django.urls import path

from .views import Dashboard

"""
This APP will be the main base frontend to connect all apps like a single page app.
"""

app_name = 'main'
urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
]
