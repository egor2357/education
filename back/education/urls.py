from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()

urlpatterns = [
  path('', include(router.urls)),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]