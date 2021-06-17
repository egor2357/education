from rest_framework import status, viewsets, views, permissions
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
  queryset = (Job.objects.all()
                          .select_related(
                            'activity',
                            'schedule__activity',
                            'specialist',
                            'method__form'
                          )
                          .prefetch_related(
                            'job_file_set',
                            'skill_report_set__skill'
                          ))
  serializer_class = JobSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = JobFilter

  def partial_update(self, request, pk=None):
    #Требует FormData для передачи файлов
    job = self.get_object()

    if 'files' in request.data:
      files = request.data.get('files', '')
      files = files.split(',') if files else []
      curr_job_files_ids = list(job.job_file_set.all().values_list('id', flat=True))
      files_to_save = []
      remaining_files = []
      for file in files:
        if file in request.FILES:
          file_data = request.FILES[file]
          files_to_save.append(Job_file(job=job, file=file_data))
        else:
          remaining_files.append(int(file))
      Job_file.objects.exclude(pk__in=remaining_files).delete()
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

      specialist = Specialist.get_available(template, curr_date)

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

    specialist = Specialist.get_available(template, date)

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
  queryset = Option_file.objects.all()
  serializer_class = Option_fileSerializer

class OptionView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  serializer_class = OptionSerializer

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return (Option.objects.all()
                            .prefetch_related('option_file_set'))
    else:
      if user.specialist is None:
        return Option.objects.none()
      else:
        return (Option.objects.filter(specialist=user.specialist)
                              .prefetch_related('option_file_set'))

class PresenceView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication, IsAdminOrReadOnly)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Presence.objects.all().select_related('main_interval', 'presence')
  serializer_class = PresenceSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = PresenceFilter

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
  filter_backends = (DjangoFilterBackend,)
  filterset_class = Skill_reportFilter

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
