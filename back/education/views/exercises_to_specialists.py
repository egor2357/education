from rest_framework import status, permissions, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from education.models import (
  Specialist, Exercise, Educational_area, Development_direction, Skill, Result
)
from education.permissions import IsAdminOrReadOnly
from education.serializers import RemoveExerciseSerializer


class Exercises_to_specialistsView(viewsets.GenericViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  def get_serializer_class(self):
    if self.action == 'remove_exercise':
      return RemoveExerciseSerializer

  @action(
    detail=False, methods=['post'],
    permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
  )
  def remove_exercise(self, request, *args, **kwargs):
    try:
      exercise = Exercise.objects.get(pk=request.data['exercise'])
    except:
      raise serializers.ValidationError(
        'Ошибка получения упражнения'
      )
    specialists = Specialist.objects.filter(pk__in=request.data['specialists'])

    exercise.specialists.remove(*specialists)
    return Response({}, status=status.HTTP_204_NO_CONTENT)

  @action(
    detail=False, methods=['post'],
    permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
  )
  def set_exercise(self, request, *args, **kwargs):
    try:
      exercise = Exercise.objects.get(pk=request.data['exercise'])
    except:
      raise serializers.ValidationError(
        'Ошибка получения упражнения'
      )
    specialists = Specialist.objects.filter(pk__in=request.data['specialists'])

    exercise.specialists.add(*specialists)
    return Response({}, status=status.HTTP_200_OK)
