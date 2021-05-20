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
