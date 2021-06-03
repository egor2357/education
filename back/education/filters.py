import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet

from .views import *

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