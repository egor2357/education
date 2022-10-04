from rest_framework import status, viewsets, views, filters, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q, Count


from django.contrib.auth import login, logout

from .models import *
from .permissions import *
from .serializers import *
from .filters import *
from .service import (
  option_update_related, job_update_related, check_presence_clashes,

  send_messages_after_list_mission, send_messages_after_create_mission,
  send_messages_after_update_mission, send_messages_after_delete_mission,
  send_messages_after_execute_mission,

  send_messages_after_create_announcement, send_messages_after_update_announcement,
  send_messages_after_delete_announcement,

  send_messages_after_create_appeal, send_messages_after_delete_appeal,
  send_messages_after_close_appeal,


)

class CreateListRetrieveDestroyViewSet(mixins.CreateModelMixin,
                                        mixins.ListModelMixin,
                                        mixins.RetrieveModelMixin,
                                        mixins.DestroyModelMixin,
                                        viewsets.GenericViewSet):
  '''
    ViewSet without update actions
  '''
  pass



# Create your views here.
class UserView(viewsets.ModelViewSet):
  queryset = User.objects.all().prefetch_related('specialist')
  serializer_class = UserSerializer
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)

  @action(detail=False)
  def current(self, request, *args, **kwargs):
    return Response(UserSerializer(request.user).data)

  @action(detail=False)
  def logout(self, request, *args, **kwargs):
    logout(request)
    return Response()

  @action(
    detail=False, methods=['post',],
    permission_classes=(permissions.AllowAny,),
    serializer_class=LoginSerializer
  )
  def login(self, request, *args, **kwargs):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request, user)
    return Response(UserSerializer(user).data)

class Educational_areaView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Educational_area.objects.all().prefetch_related('development_direction_set__skill_set__direction__area')
  serializer_class = Educational_areaSerializer

class Development_directionView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Development_direction.objects.all().prefetch_related('skill_set__direction__area')
  serializer_class = Development_directionSerializer

class SkillView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Skill.objects.all().select_related('direction__area')
  serializer_class = SkillSerializer

class FormView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Form.objects.all().prefetch_related('method_set')
  serializer_class = FormSerializer

class MethodView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Method.objects.all().select_related('form')
  serializer_class = MethodSerializer

class JobView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = JobSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = JobFilter

  def partial_update(self, request, pk=None):
    #Требует FormData для передачи файлов
    job = self.get_object()

    serializer = JobSerializer(job, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      job_update_related(job, request)
      job.refresh_from_db()
      serializer = JobSerializer(job)

    return Response(serializer.data)


  @classmethod
  def get_between(self, start_date, end_date):
    jobs = self.queryset
    jobs = jobs.filter(date__gte=start_date, date__lte=end_date)

    job_by_day_dict = {}
    for job in jobs:
      key = job.date.strftime('%d.%m.%Y')
      job_serialized = self.serializer_class(job).data
      if key not in job_by_day_dict.keys():
        job_by_day_dict[key] = [job_serialized]
      else:
        job_by_day_dict[key].append(job_serialized)

    jobs_by_day_arr = []
    curr_date = start_date
    while curr_date <= end_date:
      date_str = curr_date.strftime('%d.%m.%Y')
      obj = {
        'date': curr_date.isoformat(),
        'jobs': job_by_day_dict.get(date_str, [])
      }
      jobs_by_day_arr.append(obj)
      curr_date = curr_date + datetime.timedelta(days=1)

    return jobs_by_day_arr

  def get_queryset(self):
    jobs_qs = Job.objects.all()

    return (
      jobs_qs.select_related(
        'activity',
        'schedule__activity',
        'specialist'
      )
      .prefetch_related(
        'job_file_set',
        'skill_report_set__skill__direction__area',
        'methods__form',
      )
      .annotate(
        filled_reports_count=Count('skill_report', filter=Q(skill_report__mark__isnull=False))
      )
    )

class ScheduleView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Schedule.objects.all().select_related('activity')
  serializer_class = ScheduleSerializer

  @action(
    detail=False, methods=['post'],
    permission_classes=(permissions.IsAuthenticated, IsAdminOrReadOnly),
    serializer_class=OnlyDateSerializer
  )
  def set_for_the_week(self, request, *args, **kwargs):
    serializer = OnlyDateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    start_date = serializer.validated_data['date']
    if start_date.weekday() != 0:
      return Response(data={}, status=400)

    end_date = start_date + datetime.timedelta(days=6)

    jobs = (Job.objects.filter(date__gte=start_date, date__lte=end_date)
                        .exclude(schedule=None))
    jobs_schedule_ids = jobs.values_list('schedule_id', flat=True)

    templates = self.queryset.exclude(pk__in=jobs_schedule_ids)

    new_jobs = []
    for template in templates:
      curr_date = start_date + datetime.timedelta(days=template.day)

      specialist = Specialist.get_available(template.activity, curr_date)

      new_job = Job(activity=template.activity,
                    specialist=specialist,
                    schedule=template, date=curr_date,
                    start_time=template.start_time, comment='')
      new_jobs.append(new_job)

    Job.objects.bulk_create(new_jobs)

    return Response(data={}, status=200)

  @action(
    detail=True, methods=['post'],
    permission_classes=(permissions.IsAuthenticated, IsAdminOrReadOnly),
    serializer_class=OnlyDateSerializer
  )
  def set_for_the_day(self, request, *args, **kwargs):
    template = self.get_object()

    serializer = OnlyDateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    date = serializer.validated_data['date']


    weekday_match = template.day == date.weekday()
    if not weekday_match:
      return Response('Дни недели не совпадают')

    job_qs = Job.objects.filter(date=date, schedule=template)

    was_scheduled = job_qs.exists()
    if was_scheduled:
      job = job_qs[0]
      return Response(JobSerializer(job).data)

    specialist = Specialist.get_available(template.activity, date)

    new_job = Job(activity=template.activity,
                  specialist=specialist,
                  schedule=template, date=date,
                  start_time=template.start_time, comment='')
    new_job.save()

    return Response(JobSerializer(new_job).data)

class ActivityView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  serializer_class = ActivitySerializer
  queryset = Activity.objects.all().prefetch_related('skills')

  @action(detail=True, methods=['get'], serializer_class=Activity_skillSerializer)
  def skills(self, request, *args, **kwargs):
    activity = self.get_object()
    serializer = ActivitySerializer(activity, fields=['skills'])
    return Response(serializer.data)

  @skills.mapping.put
  def add_skill(self, request, *args, **kwargs):
    activity = self.get_object()
    serializer = Activity_skillSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    skill = serializer.validated_data['skill_id']
    activity.skills.add(skill)
    return Response(ActivitySerializer(activity, fields=['skills']).data)

  @skills.mapping.delete
  def delete_skill(self, request, *args, **kwargs):
    activity = self.get_object()
    serializer = Activity_skillSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    skill = serializer.validated_data['skill_id']
    activity.skills.remove(skill)
    return Response(ActivitySerializer(activity, fields=['skills']).data)

class Option_fileView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrOption_fileOwnerOrNoUpdateDelete)
  serializer_class = Option_fileSerializer
  queryset = Option_file.objects.all()

class OptionView(viewsets.ModelViewSet):
  permission_classes = (
    permissions.IsAuthenticated,
    IsAdminOrOptionOwnerOrNoUpdateDelete,
    CreateOptionIfHaveSpecialtyOrIsAdmin,
  )
  serializer_class = OptionSerializer
  queryset = (
    Option.objects.all()
                  .prefetch_related(
                    'option_file_set',
                    'skills__direction__area',
                    'methods__form',
                  )
  )
  filter_backends = (DjangoFilterBackend,)
  filterset_class = OptionFilter

  def partial_update(self, request, pk=None):
    option = self.get_object()

    serializer = OptionSerializer(option, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      option_update_related(option, request)
      option.refresh_from_db()
      serializer = OptionSerializer(option, context={'request': request})

    return Response(serializer.data)

  def create(self, request, pk=None):
    serializer = OptionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
      option = serializer.save(specialist=request.user.specialist)
      option_update_related(option, request)
      option.refresh_from_db()
    return Response(OptionSerializer(option, context={'request': request}).data, status=201)

def presence_create(request, summary=''):
  serializer = PresenceSerializer(data=request.data)
  if not serializer.is_valid(raise_exception=True):
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  with_quarantine = serializer.validated_data.pop('with_quarantine', False)
  quarantine_days = serializer.validated_data.pop('quarantine_days', 0)

  date_from = serializer.validated_data.pop('date_from')
  date_to = serializer.validated_data.pop('date_to')
  specialist = serializer.validated_data.pop('specialist')

  check_presence_clashes(
    specialist,
    date_from, date_to
  )

  presence_start = date_from

  if with_quarantine and (quarantine_days != 0):
    quarantine_start = date_from
    quarantine_end = quarantine_start + datetime.timedelta(days=quarantine_days-1)
    quarantine = Presence(
      specialist=specialist,
      main_interval=None,
      date_from=quarantine_start,
      date_to=quarantine_end,
      is_available=False,
      summary=summary,
    )
    quarantine.save()

    presence_start = quarantine_end + datetime.timedelta(days=1)

  presence = Presence(
    specialist=specialist,
    main_interval=None,
    date_from=presence_start,
    date_to=date_to,
    is_available=True,
    summary=summary,
  )

  presence.save()

  if with_quarantine and (quarantine_days != 0):
    quarantine.main_interval = presence
    quarantine.save()

  presence.set_jobs()

  serializer = PresenceSerializer(presence)
  return serializer

class PresenceView(viewsets.ModelViewSet):
  permission_classes = (
    permissions.IsAuthenticated,
    IsAdminOrReadPartialUpdateOnly,
  )
  filter_backends = (DjangoFilterBackend,)
  filterset_class = PresenceFilter
  queryset = Presence.objects.all().select_related('main_interval', 'presence')

  def get_serializer_class(self):
    if self.request.method == 'PATCH':
      return PresenceSummarySerializer
    else:
      return PresenceSerializer

  def create(self, request):
    serializer = presence_create(request)
    return Response(serializer.data, status=201)

  def update(self, request, pk=None):
    instance = self.get_object()
    summary = instance.summary

    instance.clear_jobs()

    presence = instance
    if presence.main_interval != None:
      presence = presence.main_interval

    instance.delete()

    Specialist.set_to_period(presence.date_from, presence.date_to)

    serializer = presence_create(request, summary)

    return Response(serializer.data, status=200)

  def partial_update(self, request, pk=None):
    serializer = PresenceSummarySerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    presence = self.get_object()
    # summary правим только у основного времени пребывания, у карантина нет summary
    # presence.summary = serializer.validated_data['summary']
    presence.save()

    if presence.main_interval != None:
      presence = presence.main_interval

    presence.summary = serializer.validated_data['summary']
    presence.save()

    serializer = PresenceSerializer(presence)

    return Response(serializer.data, status=200)

  def destroy(self, request, *args, **kwargs):
    presence = self.get_object()

    if presence.main_interval != None:
      presence = presence.main_interval
    date_from=presence.date_from
    date_to=presence.date_to

    presence.clear_jobs()

    res = super(PresenceView, self).destroy(request, *args, **kwargs)

    Specialist.set_to_period(date_from, date_to)
    return res

class SpecialistView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = (Specialist.objects.all().filter(is_active=True)
                                  .select_related('user')
                                  .prefetch_related(
                                    'specialty_set__activity',
                                    'presence_set__presence',
                                    'presence_set__main_interval'
                                  ))
  serializer_class = SpecialistSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = SpecialistFilter

  def destroy(self, request, *args, **kwargs):
    specialist = self.get_object()
    user = specialist.user
    specialist.is_active = False
    specialist.save()
    if not (user is None):
      user.delete()

    specialist.presence_set.all().delete()

    specialist.refresh_from_db()
    return Response(SpecialistSerializer(specialist).data, status=204)

class Job_fileView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Job_file.objects.all()
  serializer_class = Job_fileSerializer

class Skill_reportView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = Skill_reportSerializer
  filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
  filterset_class = Skill_reportFilter
  ordering_fields = ['job__date', 'job__activity__name', 'job__specialist__surname']

  def get_queryset(self):
    qs =  Skill_report.objects.all()

    return qs.select_related(
                              'skill__direction__area',
                              'job__activity',
                              'job__specialist',
                            )

  @action(detail=False, methods=['get'])
  def statistics(self, request, *args, **kwargs):
    skill_reports = self.filter_queryset(self.get_queryset())
    skill_reports = skill_reports.select_related(None)

    skill_reports = skill_reports.values('skill_id', 'mark')

    mark_coeffs = [0.33, 0.66, 1]
    calls_by_id = {}

    for skill_report in skill_reports:
      skill_id = skill_report['skill_id']

      if not skill_id in calls_by_id.keys():
        calls_by_id[skill_id] = {
          'planned': 0,
          'called': 0,
          'value': 0,
        }

      call = calls_by_id[skill_report['skill_id']]

      call['planned'] += 1

      if not skill_report['mark'] is None:
        call['called'] += 1
        call['value'] += mark_coeffs[skill_report['mark']]

    for skill_id in calls_by_id.keys():
      calls_by_id[skill_id]['value'] = round(calls_by_id[skill_id]['value'] / calls_by_id[skill_id]['planned'], 2)

    return Response(calls_by_id)


class SpecialtyView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  serializer_class = SpecialtySerializer

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return Specialty.objects.all().select_related('activity')
    else:
      if user.specialist is None:
        return Specialty.objects.none()
      else:
        return (Specialty.objects.filter(specialist=user.specialist)
                                  .select_related('activity'))

  def destroy(self, request, *args, **kwargs):
    specialty = self.get_object()
    specialty.reset_jobs()

    return super(SpecialtyView, self).destroy(request, *args, **kwargs)

  def create(self, request, pk=None):
    serializer = SpecialtySerializer(data=request.data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
      specialty = serializer.save()

    specialty.fill_jobs()

    return Response(SpecialtySerializer(specialty, context={'request': request}).data, status=201)


class MissionView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  serializer_class = MissionSerializer
  filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
  filterset_class = MissionFilter
  pagination_class = CommonPagination
  ordering_fields = ['creation_date', 'status', 'deadline']

  def get_queryset(self):
    user = self.request.user
    qs = Mission.objects.none()
    if user.is_staff:
      qs = Mission.objects.all()
    else:
      if user.specialist is not None:
        user_is_an_executor = Q(executor=user.specialist)
        user_is_a_controler = Q(controller=user.specialist)
        qs = Mission.objects.filter(user_is_an_executor | user_is_a_controler)
    return qs.select_related('director', 'executor', 'controller')

  def list(self, request):
    qs = self.get_queryset()
    user = self.request.user
    if (not user.is_staff) and (user.specialist is not None):
      new_missions = qs.filter(executor=user.specialist, status=0)
      send_messages_after_list_mission(new_missions)
      new_missions.update(status=1)

    notifications = Notification.objects.filter(user_id = user.id, type = 0)
    notifications._raw_delete(notifications.db)
    return super().list(request)

  def perform_create(self, serializer):
    user = self.request.user
    if user.specialist is not None:
      serializer.save(director=user.specialist)
    send_messages_after_create_mission(serializer)


  def perform_update(self, serializer):
    serializer.save()
    send_messages_after_update_mission(serializer)

  def perform_destroy(self, instance):
    notifications = Notification.objects.filter(type=0, meta__contains="{\"mission_id\": %s}" % instance.id)
    notifications._raw_delete(notifications.db)
    instance.delete()
    send_messages_after_delete_mission(instance)

  @action(
    detail=True, methods=['get'],
    permission_classes=(permissions.IsAuthenticated,),
    serializer_class=MissionSerializer
  )
  def execute(self, request, *args, **kwargs):
    user = self.request.user
    mission = self.get_object()

    if (user.specialist is not None
      and
      (mission.director == user.specialist) or (mission.controller == user.specialist)):
      mission.status = 2
      mission.save()
      serializer = MissionSerializer(mission)
      send_messages_after_execute_mission(mission, user)
      return Response(serializer.data, status=200)
    else:
      return Response({'error': 'Вы не имеете права ставить отметку о выполнении этой задачи.'}, status=400)


class AnnouncementView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  serializer_class = AnnouncementSerializer
  queryset = Announcement.objects.all()
  filter_backends = (DjangoFilterBackend,)
  filterset_class = AnnouncementFilter
  pagination_class = CommonPagination

  def list(self, request):
    notifications = Notification.objects.filter(user_id = request.user.id, type = 2)
    notifications._raw_delete(notifications.db)
    return super().list(request)

  def perform_create(self, serializer):
    serializer.save()
    send_messages_after_create_announcement(self.request, serializer)

  def perform_update(self, serializer):
    serializer.save()
    send_messages_after_update_announcement(self.request)

  def perform_destroy(self, instance):
    notifications = Notification.objects.filter(type=2, meta__contains="{\"announcement_id\": %s}" % instance.id)
    notifications._raw_delete(notifications.db)
    instance.delete()
    send_messages_after_delete_announcement(self.request)

class AppealView(CreateListRetrieveDestroyViewSet):
  permission_classes = (permissions.IsAuthenticated, NotDeleteIfNotAdmin)
  serializer_class = AppealSerializer
  filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
  filterset_class = AppealFilter
  pagination_class = CommonPagination
  ordering_fields = ['creation_date', 'creator_id']

  def get_queryset(self):
    user = self.request.user
    qs = Appeal.objects.none()
    if user.is_staff:
      qs = Appeal.objects.all()
    else:
      if user.specialist is not None:
        qs = Appeal.objects.filter(creator=user.specialist)
    return qs.select_related('creator')

  def perform_create(self, serializer):
    user = self.request.user
    if user.specialist is not None:
      serializer.save(creator=user.specialist)
    send_messages_after_create_appeal()

  def perform_destroy(self, instance):
    notifications = Notification.objects.filter(type=1, meta__contains="{\"appeal_id\": %s}" % instance.id)
    notifications._raw_delete(notifications.db)
    send_messages_after_delete_appeal(instance)
    instance.delete()

  @action(
    detail=True, methods=['get'],
    permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
    serializer_class=AppealSerializer
  )
  def close(self, request, *args, **kwargs):
    appeal = self.get_object()
    appeal.closed = True
    appeal.save()
    send_messages_after_close_appeal(appeal)
    return Response(status=200)


  @action(
    detail=True, methods=['get'],
    permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
    serializer_class=AppealSerializer
  )
  def open(self, request, *args, **kwargs):
    appeal = self.get_object()

    appeal.closed = False
    appeal.save()
    serializer = AppealSerializer(appeal)
    return Response(serializer.data, status=200)

class MessageView(CreateListRetrieveDestroyViewSet):
  permission_classes = (permissions.IsAuthenticated, NotDeleteIfNotAdmin)
  serializer_class = MessageSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = MessageFilter
  #pagination_class = CommonPagination

  def get_queryset(self):
    user = self.request.user
    qs = Message.objects.none()
    if user.is_staff:
      qs = Message.objects.all()
    else:
      if user.specialist is not None:
        qs = Message.objects.filter(appeal__creator=user.specialist)
    return qs.select_related('author')

  def list(self, request):
    if ('appeal_id') in request.query_params:
      notifications = Notification.objects\
        .filter(user_id=request.user.id, type=1,
                meta__contains="{\"appeal_id\": %s}" % request.query_params['appeal_id'])
      notifications._raw_delete(notifications.db)
    return super().list(request)

  def perform_create(self, serializer):
    user = self.request.user
    if user.specialist is not None:
      serializer.save(author=user.specialist, reply=user.is_staff)

class Task_groupView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadCreateOnly)
  filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
  queryset = Task_group.objects.all()
  filterset_class = Task_groupFilter
  pagination_class = CommonPagination
  ordering_fields = ['creation_date', 'deadline']

  def perform_create(self, serializer):
    user = self.request.user
    anonymously = serializer.validated_data.pop('anonymously', False)
    if (not anonymously) and (user.specialist is not None):
      serializer.save(author=user.specialist)
    else:
      serializer.save()

  def get_serializer_class(self):
    user = self.request.user
    if user.is_staff:
      return Task_groupAdminSerializer
    else:
      return Task_groupUserSerializer

class TalentView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadCreateOnly)
  serializer_class = TalentSerializer
  filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
  queryset = Talent.objects.all()
  filterset_class = TalentFilter
  pagination_class = CommonPagination
  ordering_fields = ['creation_date', 'area_id', 'specialist_id']

  def perform_create(self, serializer):
    user = self.request.user
    if user.specialist is not None:
      serializer.save(specialist=user.specialist)

class EducationalAreasAllView(viewsets.GenericViewSet, mixins.ListModelMixin):
  permission_classes = (permissions.IsAuthenticated, )
  queryset = Educational_area.objects.all()
  serializer_class = EducationalAreaOnlySerializer


class NotificationView(viewsets.GenericViewSet, mixins.ListModelMixin):
  permission_classes = (permissions.IsAuthenticated, )
  queryset = Notification.objects.all()
  serializer_class = NotificationSerializer

  def list(self, request):
    self.queryset = self.get_queryset().filter(user=self.request.user)
    return super().list(request)

  @action(detail=False)
  def calculated(self, request, *args, **kwargs):
    result = {}
    result['user_id'] = request.user.id
    for type in Notification.type_choices:
      result[type[0]] = Notification.objects.filter(user_id = request.user.id, type=type[0]).count()
    return Response(result)

