from rest_framework import status, viewsets, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import login, logout

from .models import *
from .serializers import *
from .filters import *

from dateutil.relativedelta import relativedelta

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
  queryset = User.objects.all()
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
    permission_classes = (permissions.AllowAny,), serializer_class = LoginSerializer
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
  queryset = Educational_area.objects.all()
  serializer_class = Educational_areaSerializer

class Development_directionView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Development_direction.objects.all()
  serializer_class = Development_directionSerializer

class SkillView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Skill.objects.all()
  serializer_class = SkillSerializer

class FormView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Form.objects.all()
  serializer_class = FormSerializer

class MethodView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Method.objects.all()
  serializer_class = MethodSerializer

class ScheduleView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Schedule.objects.all()
  serializer_class = ScheduleSerializer

class ActivityView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Activity.objects.all()
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
  queryset = Option.objects.all()
  serializer_class = OptionSerializer

class PresenceView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication, IsAdminOrReadOnly)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Presence.objects.all()
  serializer_class = PresenceSerializer

class SpecialistView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  queryset = Specialist.objects.all()
  serializer_class = SpecialistSerializer

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

class JobView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Job.objects.all()
  serializer_class = JobSerializer
  filter_backends = (DjangoFilterBackend,)
  filterset_class = JobFilter

  def get_between(start_date, end_date):
    jobs = Job.objects.filter(date__gte=start_date, date__lte=end_date)
    job_by_day_dict = {}
    for job in jobs:
      key = job.date.strftime('%d.%m.%Y')
      job_serialized = JobSerializer(job).data
      if key not in job_by_day_dict.keys():
        job_by_day_dict[key] = [job_serialized]
      else:
        job_by_day_dict[key].append(job_serialized)

    return job_by_day_dict

  @action(
    detail=False, methods=['get'],
    permission_classes=(permissions.IsAuthenticated, IsAdminOrReadOnly),
    serializer_class=WeekJobSerializer
  )
  def week(self, request, *args, **kwargs):
    serializer = WeekJobSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    start_date = serializer.validated_data['date']
    end_date = start_date + relativedelta(days=7)

    return Response(Job.get_between(start_date, end_date))

  @week.mapping.post
  def set_jobs(self, request, *args, **kwargs):
    serializer = WeekJobSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    start_date = serializer.validated_data['date']
    end_date = start_date + relativedelta(days=7)

    jobs = (Job.objects.filter(date__gte=start_date, date__lte=end_date)
                        .exclude(schedule=None))
    jobs_schedule_ids = jobs.values_list('schedule_id', flat=True)

    new_jobs = []

    templates = Schedule.objects.exclude(pk__in=jobs_schedule_ids)
    for template in templates:
      tdelta = start_date.weekday() - template.day
      curr_date = start_date + relativedelta(days=tdelta)

      available_specs_ids = (template.activity.Specialty_set.filter(is_main=True)
                                                            .values_list('specialist_id', flat=True))
      presense_specs_ids = Presence.objects.filter(
        specialist_id__in=available_specs_ids,
        date_from__gte=start_date,
        date_to__lte=end_date,
        is_available=True
      ).values_list('specialist_id', flat=True)

      specs = Specialist.objects.filter(pk__in=presense_specs_ids)
      if specs.exists():
        specialist = specs.first()
      else:
        specialist = None

      new_job = Job(option=None, activity=template.activity,
                    specialist=specialist,
                    schedule=template, date=curr_date,
                    start_time=template.start_time, comment='')

      new_jobs.append(new_job)

    Job.objects.bulk_create(new_jobs)

    return Response(Job.get_between(start_date, end_date))


class CompetenceView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  serializer_class = CompetenceSerializer

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return Competence.objects.all()
    else:
      if user.specialist is None:
        return Competence.objects.none()
      else:
        return Competence.objects.filter(specialist=user.specialist)

class SpecialtyView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  serializer_class = SpecialtySerializer

  def get_queryset(self):
    user = self.request.user
    if user.is_staff:
      return Specialty.objects.all()
    else:
      if user.specialist is None:
        return Specialty.objects.none()
      else:
        return Specialty.objects.filter(specialist=user.specialist)