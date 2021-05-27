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
  queryset = Skill.objects.all()
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
                            'specialist'
                          )
                          .prefetch_related(
                            'job_file_set',
                            'skill_report_set'
                          ))
  serializer_class = JobSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = JobFilter

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
    end_date = start_date + datetime.timedelta(days=7)

    jobs = (Job.objects.filter(date__gte=start_date, date__lte=end_date)
                        .exclude(schedule=None))
    jobs_schedule_ids = jobs.values_list('schedule_id', flat=True)

    templates = self.queryset.exclude(pk__in=jobs_schedule_ids)

    new_jobs = []
    for template in templates:
      days = start_date.weekday() - template.day
      if days < 0:
        days = 7 + days
      curr_date = start_date + datetime.timedelta(days=days)

      specialist = Specialist.get_available(template, curr_date)

      new_job = Job(activity=template.activity,
                    specialist=specialist,
                    schedule=template, date=curr_date,
                    start_time=template.start_time, comment='')
      new_jobs.append(new_job)

    Job.objects.bulk_create(new_jobs)

    return Response(JobView.get_between(start_date, end_date))

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
  queryset = Activity.objects.all().prefetch_related('skills')
  serializer_class = ActivitySerializer

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
  queryset = (Option.objects.all()
                            .prefetch_related('option_file_set'))
  serializer_class = OptionSerializer

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
  queryset = (Specialist.objects.all()
                                  .select_related('user')
                                  .prefetch_related(
                                    'competence_set__skill',
                                    'specialty_set__activity',
                                    'presence_set'
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
    return Response(SpecialistSerializer(specialist).data)

class Job_fileView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Job_file.objects.all()
  serializer_class = Job_fileSerializer

class Skill_reportView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Skill_report.objects.all()
  serializer_class = Skill_reportSerializer

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
