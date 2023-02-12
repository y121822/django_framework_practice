import os

from django.urls import path, reverse_lazy
from django.views.static import serve

from . import views

app_name = 'ads'

urlpatterns = [
    path('', views.AdListView.as_view(), name='all'),
    path('favicon.ico', serve, {'path': 'favicon.ico', 'document_root': os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'static')}),
    path('ad/<int:pk>', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad/create', views.AdCreateView.as_view(), name='ad_create'),
    path('ad/<int:pk>/update', views.AdUpdateView.as_view(), name='ad_update'),
    path('ad/<int:pk>/delete', views.AdDeleteView.as_view(success_url=reverse_lazy('ads:all')), name='ad_delete'),
    path('ad_picture/<int:pk>', views.stream_file, name='ad_picture'),
    path('ad/<int:pk>/comment', views.CommentCreateView.as_view(), name='ad_comment_create'),
    path('comment/<int:pk>/delete', views.CommentDeleteView.as_view(success_url=reverse_lazy('ads:all')),
         name='ad_comment_delete'),
    path('ad/<int:pk>/favorite', views.AddFavoriteView.as_view(), name='ad_favorite'),
    path('ad/<int:pk>/unfavorite', views.DeleteFavoriteView.as_view(), name='ad_unfavorite'),
]
