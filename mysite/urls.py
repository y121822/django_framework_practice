from django.contrib import admin
from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('', include('ads.urls')),
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login_social.html')),
    path('accounts/register/', views.SignUpView.as_view(), name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
]
