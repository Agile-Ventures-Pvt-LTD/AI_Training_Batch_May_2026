from django.urls import path, include
from django.views.static import serve
import os

urlpatterns = [
    path('api/', include('api.urls')),
]

if os.getenv('DEBUG', 'True') == 'True':
    urlpatterns += [
        path('static/<path:path>', serve, {'document_root': os.path.join(os.path.dirname(__file__), '../staticfiles')}),
    ]
