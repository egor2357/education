from rest_framework import status, viewsets, views, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import login, logout

from .models import *
from .serializers import *
from .filters import *

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
  queryset = (Educational_area.objects.all()
                                      .prefetch_related(
                                        'development_direction_set__skill_set'
                                      ))
  serializer_class = Educational_areaSerializer

class Development_directionView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Development_direction.objects.all().prefetch_related('skill_set')
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
  queryset = Method.objects.all()
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

    if 'files' in request.data:
      files = request.data.get('files', '')
      files = files.split(',') if files else []
      files_to_save = []
      remaining_files = []
      for file in files:
        if file in request.FILES:
          file_data = request.FILES[file]
          files_to_save.append(Job_file(job=job, file=file_data))
        else:
          remaining_files.append(int(file))
      job.job_file_set.exclude(pk__in=remaining_files).delete()
      Job_file.objects.bulk_create(files_to_save)

    if 'reports' in request.data:
      skills = request.data.get('reports', '')
      skills = [int(report) for report in skills.split(',')] if skills else []
      curr_skill_reports_ids = list(job.skill_report_set.all().values_list('skill_id', flat=True))
      skills_to_save = []
      remaining_skills = []
      for skill in skills:
        if skill not in curr_skill_reports_ids:
          skills_to_save.append(Skill_report(job=job, skill_id=skill))
        else:
          remaining_skills.append(skill)

      skill_reports_qs = job.skill_report_set.all()
      skill_reports_qs.exclude(skill_id__in=remaining_skills).delete()
      Skill_report.objects.bulk_create(skills_to_save)

    if 'marks' in request.data:
      marks = request.data.get('marks', [])
      for mark in marks:
        Skill_report.objects.filter(pk=mark['id']).update(mark=mark['mark'])


    serializer = JobSerializer(job, data=request.data, partial=True)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
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

    if option.activity != job.activity:
      return Response({}, status=400)

    if option.specialist != job.specialist:
      return Response({}, status=403)

    job.topic = option.topic
    job.comment = option.comment
    job.method = option.method

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
      files_to_save.append(Job_file(job=job, file=data_obj))
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
                    'specialist',
                    'method__form'
                  )
                  .prefetch_related(
                    'job_file_set',
                    'skill_report_set__skill'
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
    # return Response(JobView.get_between(start_date, end_date))

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

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return Activity.objects.all().prefetch_related('skills')
    else:
      if user.specialist is None:
        return Activity.objects.none()
      else:
        return (Activity.objects.filter(specialty__specialist=user.specialist)
                                  .prefetch_related('skills'))

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
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = Option_fileSerializer

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return Option_file.objects.all()
    else:
      if user.specialist is None:
        return Option_file.objects.none()
      else:
        return Option_file.objects.filter(option__specialist=user.specialist)

class OptionView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = OptionSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = OptionFilter

  def partial_update(self, request, pk=None):
    #Требует FormData для передачи файлов
    option = self.get_object()

    if 'files' in request.data:
      files = request.data.get('files', '')
      files = files.split(',') if files else []
      files_to_save = []
      remaining_files = []
      for file in files:
        if file in request.FILES:
          file_data = request.FILES[file]
          files_to_save.append(Option_file(option=option, file=file_data))
        else:
          remaining_files.append(int(file))
      option.option_file_set.exclude(pk__in=remaining_files).delete()
      Option_file.objects.bulk_create(files_to_save)

    if 'skills' in request.data:
      skills = request.data.get('skills', '')
      skills = [int(report) for report in skills.split(',')] if skills else []
      skills = Skill.objects.filter(pk__in=skills)
      option.skills.clear()
      option.skills.set(skills)

    serializer = OptionSerializer(option, data=request.data, partial=True, context={'request': request})
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      option.refresh_from_db()
      serializer = OptionSerializer(option, context={'request': request})

    return Response(serializer.data)

  def create(self, request, pk=None):
    #Требует FormData для передачи файлов

    serializer = OptionSerializer(data=request.data, context={'request': request})
    if serializer.is_valid(raise_exception=True):
      option = serializer.save()

    option.specialist = request.user.specialist

    if 'files' in request.data:
      files = request.data.get('files', '')
      files = files.split(',') if files else []
      files_to_save = []
      for file in files:
        if file in request.FILES:
          file_data = request.FILES[file]
          files_to_save.append(Option_file(option=option, file=file_data))
      Option_file.objects.bulk_create(files_to_save)

    if 'skills' in request.data:
      skills = request.data.get('skills', '')
      skills = [int(report) for report in skills.split(',')] if skills else []
      skills = Skill.objects.filter(pk__in=skills)
      option.skills.set(skills)

    option.save()
    option.refresh_from_db()
    return Response(OptionSerializer(option, context={'request': request}).data, status=201)

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return (Option.objects.all()
                            .prefetch_related('option_file_set')
                            .select_related('method__form'))
    else:
      if user.specialist is None:
        return Option.objects.none()
      else:
        return (Option.objects.filter(specialist=user.specialist)
                              .prefetch_related('option_file_set')
                              .select_related('method__form'))

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
  queryset = (Skill_report.objects.all()
                                  .select_related(
                                    'skill__direction__area',
                                    'job__activity',
                                    'job__method__form'
                                  )
                                  )
  serializer_class = Skill_reportSerializer
  filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
  filterset_class = Skill_reportFilter
  ordering_fields = ['job__date', 'job__activity__name', 'job__specialist__surname']

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


