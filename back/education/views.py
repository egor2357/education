from rest_framework import status, viewsets, views, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import login, logout

from .models import *
from .serializers import *

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
  permission_classes = (permissions.IsAuthenticated,)

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
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Educational_area.objects.all()
  serializer_class = Educational_areaSerializer

class Development_directionView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Development_direction.objects.all()
  serializer_class = Development_directionSerializer

class SkillView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Skill.objects.all()
  serializer_class = SkillSerializer

class FormView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Form.objects.all()
  serializer_class = FormSerializer

class MethodView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Method.objects.all()
  serializer_class = MethodSerializer

class ScheduleView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Schedule.objects.all()
  serializer_class = ScheduleSerializer

class ActivityView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Activity.objects.all()
  serializer_class = ActivitySerializer

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
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Presence.objects.all()
  serializer_class = PresenceSerializer

class SpecialistView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  permission_classes = (permissions.IsAuthenticated,)
  queryset = Specialist.objects.all()
  serializer_class = SpecialistSerializer

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