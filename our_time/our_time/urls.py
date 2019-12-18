from django.contrib import admin
from django.urls import path, include

from main.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='main'),
    path('admin/', admin.site.urls),
    path('todos/', include('todos.urls')),
    path('shelf/', include('books.urls')),
]
