from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from main.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='main'),
    path('admin/', admin.site.urls),
    path('todos/', include('todos.urls')),
    path('shelf/', include('books.urls')),
]
########################################
###    STATIC & MEDIA FILES - DEV    ###
########################################
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     MEDIA_URL = settings.MEDIA_URL.strip('/')
#     urlpatterns += [
#         re_path(
#             rf'^{MEDIA_URL}/(?P<path>.*)$',
#             static.serve,
#             {'document_root': settings.MEDIA_ROOT}
#         )
#     ]
