import os

from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from django.views.static import serve

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

urlpatterns = [
    path('', include('ads.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login_social.html')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('favicon.ico', serve, {'path': 'favicon.ico', 'document_root': os.path.join(BASE_DIR, 'mysite/static')}),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
]
