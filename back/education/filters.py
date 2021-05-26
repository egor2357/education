import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet

from .views import *

class JobFilter(FilterSet):
  class Meta:
    model = Job
    fields = {
      'date': ['gt', 'lt', 'exact'],
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