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
    path('trainings/', views.training_list, name='training_list'),
    path('add_training/', views.add_training, name='add_training'),
    path('training/<int:pk>/', views.training_detail, name='training_detail'),
    path('mysite/', views.mysite, name='mysite'),
    path('training/<int:training_id>/pdf/', views.generate_pdf, name='training_pdf'),
    path('maps/', views.map_view, name='map_view'),
    path('map/<int:map_id>/', views.map_detail, name='map_detail'),
    path('upload/', views.upload_map, name='upload_map')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)