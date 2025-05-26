from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('login/',  views.user_login, name='login'),
    path('logout/',  views.user_logout, name='logout'),
    path('register/', views.register_view, name='register'),
    path('main/', views.main, name='main'),
    path('', views.redirect_to_login, name = 'redirect_to_login'),
    path('profile/<str:username>/', views.view_profile, name='view_profile'),
    path('maps/', views.map_view, name='map_view'),
    path('map/<int:map_id>/', views.map_detail, name='map_detail'),
    path('maps/<int:map_id>/edit/', views.edit_map, name='edit_map'),
    path('maps/<int:map_id>/delete/', views.delete_map, name='delete_map'),
    path('upload/', views.upload_map, name='upload_map'),
    path('all_maps/', views.all_maps, name='all_maps')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)