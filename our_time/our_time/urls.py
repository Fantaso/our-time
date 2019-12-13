from django.contrib import admin
from django.urls import path, include

from main.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='main'),
    path('admin/', admin.site.urls),
    path('todo/', include('todo.urls')),
    path('shelf/', include('books.urls')),
]
