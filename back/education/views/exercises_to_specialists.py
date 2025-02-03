from rest_framework import status, permissions, viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from education.models import (
  Exercise_to_specialist,
  Specialist, Exercise, Educational_area, Development_direction, Skill, Result
)
from education.permissions import IsAdminOrReadOnly
from education.serializers import (
  Exercise_to_specialistSerializer,
  Exercise_to_specialistsSerializer,
  Result_to_specialistsSerializer,
  Skill_to_specialistsSerializer,
  Development_direction_to_specialistsSerializer,
  Educational_area_to_specialistsSerializer
)


class Exercises_to_specialistsView(viewsets.ModelViewSet):
  queryset = Exercise_to_specialist.objects.all()
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)

  def get_serializer_class(self):
    if self.action in ['remove_exercise', 'set_exercise']:
      return Exercise_to_specialistsSerializer
    if self.action in ['remove_result', 'set_result']:
      return Result_to_specialistsSerializer
    if self.action in ['remove_skill', 'set_skill']:
      return Skill_to_specialistsSerializer
    if self.action in ['remove_direction', 'set_direction']:
      return Development_direction_to_specialistsSerializer
    if self.action in ['remove_area', 'set_area']:
      return Educational_area_to_specialistsSerializer
    else:
      return Exercise_to_specialistSerializer

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
    return Response({}, status=status.HTTP_200_OK)
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

  @action(
    detail=False, methods=['post'],
    permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
  )
  def remove_result(self, request, *args, **kwargs):
    try:
      result = Result.objects.get(pk=request.data['result'])
    except:
      raise serializers.ValidationError(
        'Ошибка получения ожидаемого результата'
      )
    specialists = Specialist.objects.filter(pk__in=request.data['specialists'])

    exercises_id = result.exercises.all().values_list('pk', flat=True)
    Exercise_to_specialist.objects.filter(
      specialist__in=specialists, exercise_id__in=exercises_id
    ).delete()

    return Response(
      {'exercises': exercises_id},
      status=status.HTTP_200_OK
    )

  @action(
    detail=False, methods=['post'],
    permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
  )
  def set_result(self, request, *args, **kwargs):
    try:
      result = Result.objects.get(pk=request.data['result'])
    except:
      raise serializers.ValidationError(
        'Ошибка получения ожидаемого результата'
      )
    specialists = Specialist.objects.filter(pk__in=request.data['specialists'])

    exercises = result.exercises.all()
    exercises_to_specialist_to_create = []
    for specialist in specialists.prefetch_related('exercises'):
      for exercise in exercises:
        if exercise in specialist.exercises.all():
          continue
        exercises_to_specialist_to_create.append(
          Exercise_to_specialist(exercise_id=exercise.id, specialist_id=specialist.pk)
        )

    Exercise_to_specialist.objects.bulk_create(exercises_to_specialist_to_create)

    return Response(
      {'exercises': exercises.values_list('pk', flat=True)},
      status=status.HTTP_200_OK
    )