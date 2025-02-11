import datetime

from django.db.models import Prefetch, Q
from education.models import (
  Educational_area, Development_direction, Skill, Result, Exercise, Specialist, Exercise_to_option
)
from education.serializers import Educational_areaSerializer, EducationalAreaOnlySerializer
from education.permissions import IsAdminOrReadOnly
from education.querysets import getEducational_areaQueryset
from education.serializers import GetAreasByDateSerializer, GetAreasByIntervalSerializer

from rest_framework import status, viewsets, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from psycopg2._range import DateRange

from .service import UpdateRightBound

def get_prefetched_structure(param_filter, queryset):
  areas = queryset.filter(param_filter)

  directions_prefetch = Prefetch(
    'development_direction_set',
    queryset=Development_direction.objects.filter(param_filter),
    to_attr='development_direction_by_date'
  )
  skills_prefetch = Prefetch(
    'development_direction_by_date__skill_set',
    queryset=Skill.objects.filter(param_filter),
    to_attr='skill_by_date'
  )
  results_prefetch = Prefetch(
    'development_direction_by_date__skill_by_date__result_set',
    queryset=Result.objects.filter(param_filter),
    to_attr='result_by_date'
  )
  exercises_prefetch = Prefetch(
    'development_direction_by_date__skill_by_date__result_by_date__exercises',
    queryset=Exercise.objects.filter(param_filter),
    to_attr='exercises_by_date'
  )

  areas = areas.prefetch_related(
    directions_prefetch, skills_prefetch, results_prefetch, exercises_prefetch
  )
  return areas

def get_filtered_structure_by_specialist(param_filter, specialist):
  exercises_of_specialist = specialist.exercises.filter(param_filter)
  results = Result.objects.filter(param_filter, pk__in=exercises_of_specialist.values_list('result_id', flat=True))
  skills = Skill.objects.filter(param_filter, pk__in=results.values_list('skill_id', flat=True))
  directions = Development_direction.objects.filter(param_filter, pk__in=skills.values_list('direction_id', flat=True))
  areas = Educational_area.objects.filter(param_filter, pk__in=directions.values_list('area_id', flat=True))

  directions_prefetch = Prefetch(
    'development_direction_set',
    queryset=directions,
    to_attr='development_direction_filtered'
  )
  skills_prefetch = Prefetch(
    'development_direction_filtered__skill_set',
    queryset=skills,
    to_attr='skill_filtered'
  )
  results_prefetch = Prefetch(
    'development_direction_filtered__skill_filtered__result_set',
    queryset=results,
    to_attr='result_filtered'
  )
  exercises_prefetch = Prefetch(
    'development_direction_filtered__skill_filtered__result_filtered__exercises',
    queryset=exercises_of_specialist,
    to_attr='exercises_filtered'
  )

  areas = areas.prefetch_related(
    directions_prefetch, skills_prefetch, results_prefetch, exercises_prefetch
  )
  return areas

def check_if_deleted_by_date(lifetime, by_date):
  return bool(lifetime) and bool(lifetime.upper) and (lifetime.upper <= by_date)
def get_serialized_by_date_structure(areas, by_date):
  response_data = [{
    'id': area.pk,
    'name': area.name,
    'number': area.number,
    'deleted': check_if_deleted_by_date(area.lifetime, by_date),
    'development_directions': [{
      'id': direction.pk,
      'area_id': area.pk,
      'name': direction.name,
      'number': direction.number,
      'area_number': area.number,
      'deleted': check_if_deleted_by_date(direction.lifetime, by_date),
      'skills': [{
        'id': skill.pk,
        'direction_id': direction.pk,
        'area_number': area.number,
        'direction_number': direction.number,
        'name': skill.name,
        'number': skill.number,
        'deleted': check_if_deleted_by_date(skill.lifetime, by_date),
        'results': [{
          'id': result.pk,
          'skill_id': skill.pk,
          'area_number': area.number,
          'direction_number': direction.number,
          'skill_number': skill.number,
          'name': result.name,
          'number': result.number,
          'deleted': check_if_deleted_by_date(result.lifetime, by_date),
          'exercises': [{
            'id': exercise.pk,
            'result_id': result.pk,
            'area_number': area.number,
            'direction_number': direction.number,
            'skill_number': skill.number,
            'result_number': result.number,
            'name': exercise.name,
            'number': exercise.number,
            'deleted': check_if_deleted_by_date(exercise.lifetime, by_date),
          } for exercise in result.exercises_by_date]
        } for result in skill.result_by_date]
      } for skill in direction.skill_by_date]
    } for direction in area.development_direction_by_date]
  } for area in areas]

  return response_data

def get_filtered_serialized_structure(areas):
  response_data = [{
    'id': area.pk,
    'name': area.name,
    'number': area.number,
    'deleted': False,
    'development_directions': [{
      'id': direction.pk,
      'area_id': area.pk,
      'name': direction.name,
      'number': direction.number,
      'area_number': area.number,
      'deleted': False,
      'skills': [{
        'id': skill.pk,
        'direction_id': direction.pk,
        'area_number': area.number,
        'direction_number': direction.number,
        'name': skill.name,
        'number': skill.number,
        'deleted': False,
        'results': [{
          'id': result.pk,
          'skill_id': skill.pk,
          'area_number': area.number,
          'direction_number': direction.number,
          'skill_number': skill.number,
          'name': result.name,
          'number': result.number,
          'deleted': False,
          'exercises': [{
            'id': exercise.pk,
            'result_id': result.pk,
            'area_number': area.number,
            'direction_number': direction.number,
            'skill_number': skill.number,
            'result_number': result.number,
            'name': exercise.name,
            'number': exercise.number,
            'deleted': False,
          } for exercise in result.exercises_filtered]
        } for result in skill.result_filtered]
      } for skill in direction.skill_filtered]
    } for direction in area.development_direction_filtered]
  } for area in areas]

  return response_data

class Educational_areaView(viewsets.ModelViewSet):
  permission_classes = (permissions.IsAuthenticated, IsAdminOrReadOnly)
  serializer_class = Educational_areaSerializer

  def get_queryset(self):
    if self.action == 'set_end':
      return Educational_area.objects.all()
    if self.action == 'by_date':
      return Educational_area.objects.all()
    if self.action == 'by_interval':
      return Educational_area.objects.all()
    if self.action == 'by_specialist':
      return Educational_area.objects.all()
    else:
      return getEducational_areaQueryset(self.request)

  def perform_create(self, serializer):
    serializer.save(lifetime=(datetime.date.today(), None))

  def list(self, request, *args, **kwargs):
    return super(Educational_areaView, self).list(self, request, *args, **kwargs)

  @action(
    detail=True, methods=['patch'],
    permission_classes=(permissions.IsAuthenticated, permissions.IsAdminUser),
  )
  def set_end(self, request, *args, **kwargs):
    educational_area = self.get_object()
    today = datetime.date.today()
    today_str = today.strftime('%Y-%m-%d')

    # Если объект уже деактивирован, то ничего не делать
    if educational_area.lifetime and educational_area.lifetime.upper:
      return Response({}, status=status.HTTP_200_OK)

    # Если объект был создан сегодня, то удалить насовсем
    if educational_area.lifetime.lower==today or educational_area.lifetime.lower is None:
      educational_area.delete()
      return Response({}, status=status.HTTP_204_NO_CONTENT)

    educational_area.lifetime = (educational_area.lifetime.lower, today)
    educational_area.save()
    directions = educational_area.development_direction_set.all()
    skills = Skill.objects.filter(direction_id__in=directions.values_list('pk', flat=True))
    results = Result.objects.filter(skill_id__in=skills.values_list('pk', flat=True))
    exercises = Exercise.objects.filter(result_id__in=results.values_list('pk', flat=True))
    prepared_lifetime = UpdateRightBound('lifetime', right_bound=today_str)
    directions.filter(lifetime__upper=None).update(lifetime=prepared_lifetime)
    skills.filter(lifetime__upper=None).update(lifetime=prepared_lifetime)
    results.filter(lifetime__upper=None).update(lifetime=prepared_lifetime)
    exercises.filter(lifetime__upper=None).update(lifetime=prepared_lifetime)
    # Удалить упражнение из всех шаблонов занятий
    Exercise_to_option.objects.filter(exercise__in=exercises).delete()
    return Response({}, status=status.HTTP_200_OK)

  @action(
    detail=False, methods=['get'],
    permission_classes=(permissions.IsAuthenticated,),
    serializer_class=GetAreasByDateSerializer
  )
  def by_date(self, request):
    serializer = self.get_serializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    queryset = self.get_queryset()

    by_date = serializer.validated_data['by_date']
    deleted = serializer.validated_data['deleted']

    param_filter = Q(lifetime__lower__lte=by_date)

    if not deleted:
      param_filter = param_filter & ~Q(Q(lifetime__upper_inf=False) & Q(lifetime__upper__lte=by_date))

    areas = get_prefetched_structure(param_filter, queryset)
    response_data = get_serialized_by_date_structure(areas, by_date)

    return Response(response_data, status=status.HTTP_200_OK)

  @action(
    detail=False, methods=['get'],
    permission_classes=(permissions.IsAuthenticated,),
    serializer_class=GetAreasByIntervalSerializer
  )
  def by_interval(self, request):
    serializer = self.get_serializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    queryset = self.get_queryset()

    start = serializer.validated_data['start']
    end = serializer.validated_data['end']

    param_filter = Q(lifetime__overlap=DateRange(start, end, '[]'))

    areas = get_prefetched_structure(param_filter, queryset)
    response_data = get_serialized_by_date_structure(areas, end)

    return Response(response_data, status=status.HTTP_200_OK)

  @action(
    detail=False, methods=['get'],
    permission_classes=(permissions.IsAuthenticated,),
  )
  def by_specialist(self, request):
    specialist = request.user.specialist
    queryset = self.get_queryset()

    if request.user.is_staff:
      by_date = datetime.date.today()
      param_filter = Q(lifetime__lower__lte=by_date) & ~Q(Q(lifetime__upper_inf=False) & Q(lifetime__upper__lte=by_date))
      areas = get_prefetched_structure(param_filter, queryset)
      response_data = get_serialized_by_date_structure(areas, by_date)
    else:
      param_filter = Q(lifetime__upper_inf=True)
      areas = get_filtered_structure_by_specialist(param_filter, specialist)
      response_data = get_filtered_serialized_structure(areas)

    return Response(response_data, status=status.HTTP_200_OK)

class EducationalAreasAllView(viewsets.GenericViewSet, mixins.ListModelMixin):
  permission_classes = (permissions.IsAuthenticated, )
  queryset = Educational_area.objects.all()
  serializer_class = EducationalAreaOnlySerializer