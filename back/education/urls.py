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
router.register(r'option_files', Option_fileView, basename='Option_file')
router.register(r'activities', ActivityView, basename='Activity')
router.register(r'schedule', ScheduleView)
router.register(r'specialists', SpecialistView)
router.register(r'options', OptionView, basename='Option')
router.register(r'presence', PresenceView)
router.register(r'job_files', Job_fileView)
router.register(r'skill_reports', Skill_reportView, basename='Skill_report')
router.register(r'jobs', JobView, basename='Job')
router.register(r'competence', CompetenceView, basename='Competence')
router.register(r'specialties', SpecialtyView, basename='Specialty')
router.register(r'missions', MissionView, basename='Mission')
router.register(r'announcement', AnnouncementView, basename='Announcement')
router.register(r'appeals', AppealView, basename='Appeal')
router.register(r'messages', MessageView, basename='Message')
router.register(r'task_groups', Task_groupView, basename='Task_group')


urlpatterns = [
  path('', include(router.urls)),

  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]