from rest_framework import routers
from django.urls import path, include
from .views import *

router = routers.DefaultRouter()
router.register(r'users', UserView, basename='User')
router.register(r'educational_areas', Educational_areaView, basename='Educational_area')
router.register(r'educational_areas_all', EducationalAreasAllView, basename='EducationalAreasAll')
router.register(r'development_directions', Development_directionView, basename='Development_direction')
router.register(r'skills', SkillView, basename='Skill')
router.register(r'forms', FormView, basename='Form')
router.register(r'methods', MethodView, basename='Method')
router.register(r'option_files', Option_fileView, basename='Option_file')
router.register(r'activities', ActivityView, basename='Activity')
router.register(r'schedule', ScheduleView, basename='Schedule')
router.register(r'specialists', SpecialistView, basename='Specialist')
router.register(r'options', OptionView, basename='Option')
router.register(r'presence', PresenceView, basename='Presence')
router.register(r'job_files', Job_fileView, basename='Job_file')
router.register(r'skill_reports', Skill_reportView, basename='Skill_report')
router.register(r'jobs', JobView, basename='Job')
router.register(r'competence', CompetenceView, basename='Competence')
router.register(r'specialties', SpecialtyView, basename='Specialty')
router.register(r'missions', MissionView, basename='Mission')
router.register(r'announcement', AnnouncementView, basename='Announcement')
router.register(r'appeals', AppealView, basename='Appeal')
router.register(r'messages', MessageView, basename='Message')
router.register(r'task_groups', Task_groupView, basename='Task_group')
router.register(r'talents', TalentView, basename='Talent')


urlpatterns = [
  path('', include(router.urls)),

  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]