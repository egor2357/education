from rest_framework import status, viewsets, views, permissions
from rest_framework.response import Response

from django.contrib.auth import login, logout

from .models import *
from .serializers import *

from rest_framework.authentication import SessionAuthentication
class CsrfExemptSessionAuthentication(SessionAuthentication):
  def enforce_csrf(self, request):
    return

# Create your views here.
class LoginView(views.APIView):
  permission_classes = (permissions.AllowAny,)
  authentication_classes = (CsrfExemptSessionAuthentication,)
  serializer_class = LoginSerializer

  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    login(request, user)
    return Response(UserSerializer(user).data)
