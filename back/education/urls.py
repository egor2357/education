from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserView)
router.register(r'educational_areas', Educational_areaView)
router.register(r'development_directions', Development_directionView)
router.register(r'skills', SkillView)
router.register(r'forms', FormView)
router.register(r'methods', MethodView)
router.register(r'option_files', Option_fileView)
router.register(r'activities', ActivityView)
router.register(r'schedule', ScheduleView)
router.register(r'specialist', SpecialistView)
router.register(r'option', OptionView)


urlpatterns = [
  path('', include(router.urls)),

  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]