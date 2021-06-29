import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet

from .views import *
from .models import *
from .serializers import *

class JobFilter(FilterSet):
  class Meta:
    model = Job
    fields = {
      'date': ['gte', 'lte', 'gt', 'lt', 'exact'],
      'specialist_id': ['exact'],
      'activity_id': ['exact']
    }

class PresenceFilter(FilterSet):
  interval_start = django_filters.DateFilter(
    label='Начало интервала', field_name='date_to',
    lookup_expr='lt', exclude=True
  )
  interval_end = django_filters.DateFilter(
    label='Конец интервала', field_name='date_from',
    lookup_expr='gt', exclude=True
  )
  class Meta:
    model = Presence
    fields = [
      'interval_start',
      'interval_end'
    ]

class SpecialistFilter(FilterSet):
  is_active = django_filters.BooleanFilter(
    label='Активен ли', field_name='is_active',
    lookup_expr='exact'
  )
  is_staff = django_filters.BooleanFilter(
    label='Администратор ли', field_name='user__is_staff',
    lookup_expr='exact'
  )
  class Meta:
    model = Specialist
    fields = [
      'is_active',

    ]

class Skill_reportFilter(FilterSet):
  date_from = django_filters.DateFilter(
    label='Начало интервала', field_name='job',
    lookup_expr='date__gte',
  )
  date_to = django_filters.DateFilter(
    label='Конец интервала', field_name='job',
    lookup_expr='date__lte',
  )
  is_affected = django_filters.BooleanFilter(
    label='Затронут ли навык', field_name='mark',
    lookup_expr='isnull', exclude=True,
  )
  skill_id = django_filters.NumberFilter(
    label='Идентификатор навыка', field_name='skill_id',
    lookup_expr='exact'
  )
  class Meta:
    model = Skill_report
    fields = [
      'date_from',
      'date_to',
      'is_affected',
      'skill_id',
    ]

class OptionFilter(FilterSet):
  activity_id = django_filters.NumberFilter(
    label='Идентификатор вида деятельности', field_name='activity_id',
    lookup_expr='exact'
  )

  class Meta:
    model = Option
    fields = [
      'activity_id',
    ]