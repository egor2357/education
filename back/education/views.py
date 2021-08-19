from rest_framework import status, viewsets, views, permissions, filters, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q


from django.contrib.auth import login, logout

from .models import *
from .serializers import *
from .filters import *
from .service import (option_update_related, job_update_related)

from rest_framework.authentication import SessionAuthentication
class CsrfExemptSessionAuthentication(SessionAuthentication):
  def enforce_csrf(self, request):
    return

class IsAdminOrReadOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    else:
      return request.user.is_staff

class NotDeleteIfNotAdmin(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method == 'DELETE':
      return request.user.is_staff
    else:
      return True

class IsAdminOrReadCreateOnly(permissions.BasePermission):
  def has_permission(self, request, view):
    safe_methods = list(permissions.SAFE_METHODS[:])
    safe_methods.append('POST')
    if request.method in safe_methods:
      return True
    else:
      return request.user.is_staff

class IsAdminOrOptionOwnerOrNoUpdateDelete(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    user = request.user

    if user.is_staff:
      return True
    elif (user.specialist is not None) and (obj.specialist == user.specialist):
      return True
    else:
      return request.method in permissions.SAFE_METHODS

class IsAdminOrOption_fileOwnerOrNoUpdateDelete(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    user = request.user

    if user.is_staff:
      return True
    elif (user.specialist is not None) and (obj.option.specialist == user.specialist):
      return True
    else:
      return request.method in permissions.SAFE_METHODS

class CreateOptionIfHaveSpecialtyOrIsAdmin(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method == 'POST':
      user = request.user
      if user.is_staff:
        return True
      elif user.specialist is not None:
        activity_id = request.POST.get('activity_id', None)
        if activity_id is None:
          return False
        return user.specialist.activities.filter(pk=activity_id).exists()
      else:
        return False
    else:
      return True


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
  authentication_classes = (CsrfExemptSessionAuthentication,)
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
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Educational_area.objects.all().prefetch_related('development_direction_set__skill_set__direction__area')
  serializer_class = Educational_areaSerializer

class Development_directionView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Development_direction.objects.all().prefetch_related('skill_set__direction__area')
  serializer_class = Development_directionSerializer

class SkillView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Skill.objects.all().select_related('direction__area')
  serializer_class = SkillSerializer

class FormView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Form.objects.all().prefetch_related('method_set')
  serializer_class = FormSerializer

class MethodView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Method.objects.all().select_related('form')
  serializer_class = MethodSerializer

class JobView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
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

  @action(
    detail=True, methods=['patch'],
    permission_classes=(permissions.IsAuthenticated,),
    serializer_class=JobByOptionSerializer
  )
  def set_job_by_option(self, request, *args, **kwargs):
    user = self.request.user
    job = self.get_object()

    serializer = JobByOptionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    option_id = serializer.validated_data['option_id']

    try:
      option = Option.objects.get(pk=option_id)
    except:
      return Response({}, status=404)

    job.topic = option.topic
    job.comment = option.comment

    job.methods.set(option.methods.all())

    job.skill_report_set.all().delete()
    reports_to_save = []
    for skill in option.skills.filter(pk__in=user.specialist.skills.all()).distinct():
      reports_to_save.append(Skill_report(job=job, skill=skill))
    Skill_report.objects.bulk_create(reports_to_save)

    files_to_save = []
    job.job_file_set.all().delete()
    for file in option.option_file_set.all():
      data_obj = ContentFile(file.file.read())
      name = os.path.split(file.file.name)[-1]
      data_obj.name = name
      new_file = Job_file(job=job, file=data_obj)
      new_file.create_thumbnail()
      files_to_save.append(new_file)
    Job_file.objects.bulk_create(files_to_save)

    job.save()
    job.refresh_from_db()

    return Response(JobSerializer(job).data, status=200)

  def get_queryset(self):
    user = self.request.user
    jobs_qs = Job.objects.none()
    if user.is_staff:
      jobs_qs = Job.objects.all()
    else:
      jobs_qs = Job.objects.all()
      own_jobs = Q(specialist=user.specialist)
      competence_jobs = Q(reports__in=user.specialist.skills.all())
      jobs_qs = Job.objects.filter(own_jobs | competence_jobs).distinct()

    return (jobs_qs.select_related(
                    'activity',
                    'schedule__activity',
                    'specialist'
                  )
                  .prefetch_related(
                    'job_file_set',
                    'skill_report_set__skill__direction__area',
                    'methods__form',
                  ))

class ScheduleView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
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
  authentication_classes = (CsrfExemptSessionAuthentication,)
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
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrOption_fileOwnerOrNoUpdateDelete)
  serializer_class = Option_fileSerializer
  queryset = Option_file.objects.all()

class OptionView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
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

class PresenceView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication, IsAdminOrReadOnly)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Presence.objects.all().select_related('main_interval', 'presence')
  serializer_class = PresenceSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = PresenceFilter

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
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = (Specialist.objects.all().filter(is_active=True)
                                  .select_related('user')
                                  .prefetch_related(
                                    'competence_set__skill',
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
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Job_file.objects.all()
  serializer_class = Job_fileSerializer

class Skill_reportView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = Skill_reportSerializer
  filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
  filterset_class = Skill_reportFilter
  ordering_fields = ['job__date', 'job__activity__name', 'job__specialist__surname']

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      qs =  Skill_report.objects.all()
    else:
      if user.specialist is not None:
        qs = Skill_report.objects.filter(skill__in=user.specialist.skills.all())
      else:
        qs = Skill_report.objects.none()
    return qs.select_related(
                              'skill__direction__area',
                              'job__activity',
                              'job__specialist',
                            )
  @action(detail=False, methods=['get'])
  def statistics(self, request, *args, **kwargs):
    skill_reports = self.filter_queryset(self.get_queryset())

    mark_coeffs = [0.33, 0.66, 1]
    calls_by_id = {}

    for skill_report in skill_reports:
      if not skill_report.skill.id in calls_by_id.keys():
        calls_by_id[skill_report.skill.id] = {
          'planned': 0,
          'called': 0,
          'value': 0,
        }

      calls_by_id[skill_report.skill.id]['planned'] += 1

      is_called = not skill_report.mark is None
      calls_by_id[skill_report.skill.id]['called'] += 1 if is_called else 0
      calls_by_id[skill_report.skill.id]['value'] += mark_coeffs[skill_report.mark]*skill_report.coefficient if is_called else 0

    for skill_id in calls_by_id.keys():
      calls_by_id[skill_id]['value'] = round(calls_by_id[skill_id]['value'] / calls_by_id[skill_id]['planned'], 2)

    return Response(calls_by_id)

  @action(
    detail=False, methods=['get'],
    permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
    serializer_class=Skill_reportSerializer
  )
  def set_current_coefficients(self, request, *args, **kwargs):
    skill_reports = self.filter_queryset(self.get_queryset())

    coeff_by_spec_id_skill_id = {}
    all_competence = Competence.objects.all()
    for competence in all_competence:
      if not competence.specialist_id in coeff_by_spec_id_skill_id.keys():
        coeff_by_spec_id_skill_id[competence.specialist_id] = {}

      coeff_by_spec_id_skill_id[competence.specialist_id][competence.skill_id] = competence.coefficient

    absent_coeffs = []

    for skill_report in skill_reports:
      spec_id = skill_report.job.specialist_id
      skill_id = skill_report.skill_id
      try:
        skill_report.coefficient = coeff_by_spec_id_skill_id[spec_id][skill_id]
        skill_report.save()
      except:
        absent_coeffs.append(
          '{0} не имеет навыка {1}'.format(
            skill_report.job.specialist.__str__(),
            skill_report.skill.name
          )
        )

    return Response({'absent': absent_coeffs})

class CompetenceView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  serializer_class = CompetenceSerializer

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return Competence.objects.all().select_related('skill')
    else:
      if user.specialist is None:
        return Competence.objects.none()
      else:
        return (Competence.objects.filter(specialist=user.specialist)
                                  .select_related('skill'))

class SpecialtyView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
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
  authentication_classes = (CsrfExemptSessionAuthentication,)
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
      new_missions.update(status=1)
    return super().list(request)

  def perform_create(self, serializer):
    user = self.request.user
    if user.specialist is not None:
      serializer.save(director=user.specialist)

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
      return Response(serializer.data, status=200)
    else:
      return Response({'error': 'Вы не имеете права ставить отметку о выполнении этой задачи.'}, status=400)


class AnnouncementView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  serializer_class = AnnouncementSerializer
  queryset = Announcement.objects.all()
  filter_backends = (DjangoFilterBackend,)
  filterset_class = AnnouncementFilter
  pagination_class = CommonPagination

class AppealView(CreateListRetrieveDestroyViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, NotDeleteIfNotAdmin)
  serializer_class = AppealSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = AppealFilter
  pagination_class = CommonPagination

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

  @action(
    detail=True, methods=['get'],
    permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
    serializer_class=AppealSerializer
  )
  def close(self, request, *args, **kwargs):
    appeal = self.get_object()

    appeal.closed = True
    appeal.save()
    serializer = AppealSerializer(appeal)
    return Response(serializer.data, status=200)

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
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, NotDeleteIfNotAdmin)
  serializer_class = MessageSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = MessageFilter
  pagination_class = CommonPagination

  def get_queryset(self):
    user = self.request.user
    qs = Message.objects.none()
    if user.is_staff:
      qs = Message.objects.all()
    else:
      if user.specialist is not None:
        qs = Message.objects.filter(appeal__creator=user.specialist)
    return qs.select_related('author')

  def perform_create(self, serializer):
    user = self.request.user
    if user.specialist is not None:
      serializer.save(author=user.specialist, reply=user.is_staff)

class Task_groupView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadCreateOnly)
  filter_backends = (DjangoFilterBackend,)
  queryset = Task_group.objects.all()
  filterset_class = Task_groupFilter
  pagination_class = CommonPagination

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
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadCreateOnly)
  serializer_class = TalentSerializer
  filter_backends = (DjangoFilterBackend,)
  queryset = Talent.objects.all()
  filterset_class = TalentFilter
  pagination_class = CommonPagination

  def perform_create(self, serializer):
    user = self.request.user
    if user.specialist is not None:
      serializer.save(specialist=user.specialist)