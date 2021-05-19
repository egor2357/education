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

# Create your views here.
class UserView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  queryset = User.objects.all()
  serializer_class = UserSerializer

  @action(detail=False)
  def current(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return Response(UserSerializer(request.user).data)
    else:
      return Response({}, status=403)

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
  queryset = Educational_area.objects.all()
  serializer_class = Educational_areaSerializer

class Development_directionView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  queryset = Development_direction.objects.all()
  serializer_class = Development_directionSerializer

class SkillView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  queryset = Skill.objects.all()
  serializer_class = SkillSerializer

class FormView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  queryset = Form.objects.all()
  serializer_class = FormSerializer

class MethodView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  queryset = Method.objects.all()
  serializer_class = MethodSerializer

class ScheduleView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  queryset = Schedule.objects.all()
  serializer_class = ScheduleSerializer

class ActivityView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  queryset = Activity.objects.all()
  serializer_class = ActivitySerializer

class Option_fileView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  queryset = Option_file.objects.all()
  serializer_class = Option_fileSerializer

class OptionView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  queryset = Option.objects.all()
  serializer_class = OptionSerializer

class SpecialistView(viewsets.ModelViewSet):
  authentication_classes = (CsrfExemptSessionAuthentication,)
  queryset = Specialist.objects.all()
  serializer_class = SpecialistSerializer