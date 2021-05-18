from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserView)
router.register(r'educational_areas', Educational_areaView)
router.register(r'development_directions', Development_directionView)
router.register(r'skills', SkillView)

urlpatterns = [
  path('', include(router.urls)),
  path('login/', LoginView.as_view()),
  path('logout/', LogoutView.as_view()),
  path('current/', CurrentUserView.as_view()),


  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]