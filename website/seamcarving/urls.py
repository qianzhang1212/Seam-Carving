from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('resize-without-mask', views.resize, name='resize'),
    path('content-amplification', views.amplification, name='amplification'),
    path('resize-with-mask', views.mask, name='mask'),
    path('object-removal', views.removal, name='removal'),
    path('video-retargeting', views.video, name='video'),
    path('process', views.process, name='process'),
]
