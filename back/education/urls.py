from rest_framework import routers
from django.urls import path, include
from .views import (
  UserView, Educational_areaView, EducationalAreasAllView,
  Development_directionView, SkillView, ResultView, ExerciseView,
  FormView, MethodView, Option_fileView, ActivityView, ScheduleView,
  SpecialistView, OptionView, PresenceView, Job_fileView, Job_report_fileView,
  Exercise_reportView, JobView, SpecialtyView, MissionView, AnnouncementView,
  AppealView, MessageView, Task_groupView, TalentView, NotificationView,
  Exercises_to_specialistsView
)

router = routers.DefaultRouter()
router.register(r'users', UserView, basename='User')
router.register(r'educational_areas', Educational_areaView, basename='Educational_area')
router.register(r'educational_areas_all', EducationalAreasAllView, basename='EducationalAreasAll')
router.register(r'development_directions', Development_directionView, basename='Development_direction')
router.register(r'skills', SkillView, basename='Skill')
router.register(r'results', ResultView, basename='Result')
router.register(r'exercises', ExerciseView, basename='Exercise')
router.register(r'forms', FormView, basename='Form')
router.register(r'methods', MethodView, basename='Method')
router.register(r'option_files', Option_fileView, basename='Option_file')
router.register(r'activities', ActivityView, basename='Activity')
router.register(r'schedule', ScheduleView, basename='Schedule')
router.register(r'specialists', SpecialistView, basename='Specialist')
router.register(r'options', OptionView, basename='Option')
router.register(r'presence', PresenceView, basename='Presence')
router.register(r'job_files', Job_fileView, basename='Job_file')
router.register(r'job_report_files', Job_report_fileView, basename='Job_report_file')
router.register(r'exercise_reports', Exercise_reportView, basename='Exercise_report')
router.register(r'jobs', JobView, basename='Job')
router.register(r'specialties', SpecialtyView, basename='Specialty')
router.register(r'missions', MissionView, basename='Mission')
router.register(r'announcement', AnnouncementView, basename='Announcement')
router.register(r'appeals', AppealView, basename='Appeal')
router.register(r'messages', MessageView, basename='Message')
router.register(r'task_groups', Task_groupView, basename='Task_group')
router.register(r'talents', TalentView, basename='Talent')
router.register(r'notifications', NotificationView, basename='Notification')
router.register(r'exercises_to_specialists', Exercises_to_specialistsView, basename='Exercises_to_specialists')


urlpatterns = [
  path('', include(router.urls)),

  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]