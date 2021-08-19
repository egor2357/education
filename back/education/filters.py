import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.rest_framework import FilterSet
from rest_framework.pagination import PageNumberPagination

from .views import *
from .models import *
from .serializers import *


class NumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
  pass


class CommonPagination(PageNumberPagination):
  page_size = 10
  page_size_query_param = 'per_page'
  max_page_size = 1000

  def get_paginated_response(self, data):
    page_size = self.get_page_size(self.request)
    if page_size is None:
      page_size = 10
    return Response({
      'pagination': {
        'count': self.page.paginator.count,
        'page': self.page.number,
        'per_page': page_size,
        'links': {
          'next': self.get_next_link(),
          'previous': self.get_previous_link()
        },
      },
      'results': data
    })


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
  class Meta:
    model = Option
    fields = [
      'activity_id',
      'specialist_id',
    ]

class MissionFilter(FilterSet):
  creation_date = django_filters.DateFilter(
    label='Дата создания', field_name='creation_date',
    lookup_expr='date',
  )
  caption = django_filters.CharFilter(
    lookup_expr='icontains'
  )
  comment = django_filters.CharFilter(
    lookup_expr='icontains'
  )
  director_id = NumberInFilter()
  executor_id = NumberInFilter()
  controller_id = NumberInFilter()
  status = NumberInFilter()

  class Meta:
    model = Mission
    fields = [
      'status',
      'director_id', 'executor_id', 'controller_id',
      'deadline', 'creation_date',
      'caption', 'comment'
    ]

class AnnouncementFilter(FilterSet):
  caption = django_filters.CharFilter(
    lookup_expr='icontains'
  )
  text = django_filters.CharFilter(
    lookup_expr='icontains'
  )

  class Meta:
    model = Announcement
    fields = '__all__'

class AppealFilter(FilterSet):
  theme = django_filters.CharFilter(
    lookup_expr='icontains'
  )
  creation_date = django_filters.DateFilter(
    label='Дата создания', field_name='creation_date',
    lookup_expr='date',
  )

  class Meta:
    model = Appeal
    fields = (
      'creator_id',
      'theme', 'creation_date',
      'closed',
    )

class MessageFilter(FilterSet):
  text = django_filters.CharFilter(
    lookup_expr='icontains'
  )
  creation_date = django_filters.DateFilter(
    label='Дата создания', field_name='creation_date',
    lookup_expr='date',
  )

  class Meta:
    model = Message
    fields = (
      'appeal_id',
      'author_id',
      'text', 'creation_date',
      'reply',
    )

class Task_groupFilter(FilterSet):
  text = django_filters.CharFilter(
    lookup_expr='icontains'
  )
  solution = django_filters.CharFilter(
    lookup_expr='icontains'
  )
  creation_date = django_filters.DateFilter(
    label='Дата создания', field_name='creation_date',
    lookup_expr='date',
  )
  author_id = NumberInFilter()
  responsible_id = NumberInFilter()

  class Meta:
    model = Task_group
    fields = (
      'author_id', 'responsible_id',
      'text', 'solution',
      'creation_date', 'deadline',
      'is_question',
    )

class TalentFilter(FilterSet):
  name = django_filters.CharFilter(
    lookup_expr='icontains'
  )
  text = django_filters.CharFilter(
    lookup_expr='icontains'
  )
  creation_date = django_filters.DateFilter(
    label='Дата создания', field_name='creation_date',
    lookup_expr='date',
  )
  specialist_id = NumberInFilter()
  area_id = NumberInFilter()

  class Meta:
    model = Talent
    fields = (
      'specialist_id', 'area_id',
      'text',
      'creation_date',
    )