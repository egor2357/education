from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from django.db.models import Q

from .models import *

import os

#create your serializers here.

# /////////////////////////////////////////////////

class OnlyDateSerializer(serializers.Serializer):
  date = serializers.DateField(initial=datetime.date.today)

class JobByOptionSerializer(serializers.Serializer):
  option_id = serializers.IntegerField(max_value=None, min_value=1)

# /////////////////////////////////////////////////

class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):
    username = data.get('username', None)
    password = data.get('password', None)

    if username is None:
      raise serializers.ValidationError(
        'Логин пользователя не введен'
      )
    if password is None:
      raise serializers.ValidationError(
        'Пароль пользователя не введен'
      )

    user = authenticate(username=username, password=password)

    if user is None:
      raise serializers.ValidationError(
        'Логин или пароль пользователя не верен'
      )
    if not user.is_active:
      raise serializers.ValidationError(
        'Пользователь не активен'
      )

    return {'user': user}

class FilteredSkillListSerializer(serializers.ListSerializer):
  def to_representation(self, data):
    user=self.context['request'].user
    qs = Skill.objects.none()
    if user.is_staff:
      qs =  data
    else:
      if user.specialist is not None:
        qs = data.filter(competence__specialist=user.specialist)

    return super(FilteredSkillListSerializer, self).to_representation(qs)

class SkillSerializer(FlexFieldsModelSerializer):
  direction_id = serializers.PrimaryKeyRelatedField(
    source='direction', queryset=Development_direction.objects.all()
  )
  def get_area_number(self, instance):
    return instance.direction.area.number
  area_number = serializers.SerializerMethodField()

  def get_direction_number(self, instance):
    return instance.direction.number
  direction_number = serializers.SerializerMethodField()

  class Meta:
    model = Skill
    fields = (
      'id',
      'name', 'number',
      'direction_id',
      'direction_number',
      'area_number'
    )
    list_serializer_class = FilteredSkillListSerializer

class Activity_skillSerializer(serializers.ModelSerializer):
  skill_id = serializers.PrimaryKeyRelatedField(
    queryset=Skill.objects.all(), write_only=True
  )
  class Meta:
    model = Activity
    fields = ('skill_id',)

class ActivitySerializer(FlexFieldsModelSerializer):
  skills = serializers.PrimaryKeyRelatedField(
    many=True, read_only=True
  )
  class Meta:
    model = Activity
    fields = (
      'id',
      'name', 'color',
      'skills',
    )
    expandable_fields = {
      'skills': SkillSerializer,
    }

class ScheduleSerializer(serializers.ModelSerializer):
  activity_id = serializers.PrimaryKeyRelatedField(
    source='activity', queryset=Activity.objects.all(),
    many=False, write_only=True
  )
  activity = ActivitySerializer(
    read_only=True,
    omit=['skills']
  )
  class Meta:
    model = Schedule
    fields = (
      'id',
      'day', 'start_time',
      'activity_id', 'activity',
    )

class PresenceSerializer(serializers.ModelSerializer):
  specialist_id = serializers.PrimaryKeyRelatedField(
    source='specialist', queryset=Specialist.objects.all()
  )
  main_interval_id = serializers.PrimaryKeyRelatedField(
    source='main_interval', read_only=True
  )
  is_available = serializers.BooleanField(read_only=True)

  with_quarantine = serializers.BooleanField(write_only=True)
  quarantine_days = serializers.IntegerField(
    required=False,
    write_only=True, min_value=0
  )

  def get_full_interval(self, instance):
    main_interval = instance.main_interval if instance.main_interval is not None else instance

    quarantine = main_interval.presence if hasattr(main_interval, 'presence') else None
    date_from = quarantine.date_from if quarantine is not None else main_interval.date_from
    date_to = main_interval.date_to
    quarantine_days = 0 if quarantine is None else (quarantine.date_to - quarantine.date_from).days + 1
    return {'date_from': date_from, 'date_to': date_to, 'quarantine_days': quarantine_days}
  full_interval = serializers.SerializerMethodField()

  def check_spec_clashes(self, specialist, date_from, date_to):
    spec_presense_qs = Presence.objects.filter(specialist=specialist)
    clashes_qs = spec_presense_qs.exclude(date_to__lt=date_from)
    clashes_qs = clashes_qs.exclude(date_from__gt=date_to)

    if clashes_qs.exists():
      raise serializers.ValidationError(
        {
          'non_field_errors': [
            'Выбранный период пересекается с периодом {0} - {1}'
            .format(
              clashes_qs[0].date_from.strftime('%d.%m.%Y'),
              clashes_qs[0].date_to.strftime('%d.%m.%Y')
            )
          ]
        }
      )

  def validate(self, data):
    if data['date_to'] < data['date_from']:
      raise serializers.ValidationError(
        'Дата начала должна быть меньше или равна дате конца'
      )

    if data.get('with_quarantine', False):
      quarantine_days = data.get('quarantine_days', 0)
      tdelta = data['date_to'] - data['date_from']
      if tdelta.days <= quarantine_days:
        raise serializers.ValidationError(
          'Количество дней на карантине должно быть' +
          ' меньше самого срока присутствия'
        )

    return data

  def create(self, validated_data):
    with_quarantine = validated_data.pop('with_quarantine', False)
    quarantine_days = validated_data.pop('quarantine_days', 0)

    date_from = validated_data.pop('date_from')
    date_to = validated_data.pop('date_to')
    specialist = validated_data.pop('specialist')

    self.check_spec_clashes(
      specialist,
      date_from, date_to
    )

    presence_start = date_from

    if with_quarantine and (quarantine_days != 0):
      quarantine_start = date_from
      quarantine_end = quarantine_start + datetime.timedelta(days=quarantine_days-1)
      quarantine = Presence(
        specialist=specialist,
        main_interval=None,
        date_from=quarantine_start,
        date_to=quarantine_end,
        is_available=False
      )
      quarantine.save()

      presence_start = quarantine_end + datetime.timedelta(days=1)

    presence = Presence(
      specialist=specialist,
      main_interval=None,
      date_from=presence_start,
      date_to=date_to,
      is_available=True
    )

    presence.save()

    if with_quarantine and (quarantine_days != 0):
      quarantine.main_interval = presence
      quarantine.save()

    presence.set_jobs()

    return presence

  def update(self, instance, validated_data):
    instance.clear_jobs()

    presence = instance
    if presence.main_interval != None:
      presence = presence.main_interval

    instance.delete()

    Specialist.set_to_period(presence.date_from, presence.date_to)

    return self.create(validated_data)

  class Meta:
    model = Presence
    fields = (
      'id',
      'specialist_id',
      'main_interval_id',
      'date_from', 'date_to',
      'is_available',
      'full_interval',
      'with_quarantine', 'quarantine_days'
    )

class SpecialistSerializer(FlexFieldsModelSerializer):
  class Meta:
    model = Specialist
    fields = (
      'id',
      'surname', 'name',
      'patronymic', 'role',
    )

class UserSerializer(FlexFieldsModelSerializer):
  specialist = SpecialistSerializer(read_only=True)
  class Meta:
    model = User
    fields = [
      'id',
      'username', 'is_staff',
      'specialist'
    ]

class SpecialtySerializer(FlexFieldsModelSerializer):
  activity_id = serializers.PrimaryKeyRelatedField(
    source='activity', queryset=Activity.objects.all()
  )
  activity = ActivitySerializer(
    read_only=True,
    fields=['id', 'name', 'color']
  )
  specialist_id = serializers.PrimaryKeyRelatedField(
    source='specialist', queryset=Specialist.objects.all()
  )

  is_main = serializers.BooleanField()
  class Meta:
    model = Specialty
    fields = (
      'id',
      'activity_id', 'specialist_id',
      'is_main',
      'activity'
    )

class CompetenceSerializer(FlexFieldsModelSerializer):
  skill_id = serializers.PrimaryKeyRelatedField(
    source='skill', queryset=Skill.objects.all()
  )
  skill = SkillSerializer(
    read_only=True,
    fields=['id', 'name', 'number']
  )
  specialist_id = serializers.PrimaryKeyRelatedField(
    source='specialist',queryset=Specialist.objects.all()
  )
  coefficient = serializers.FloatField(min_value= 0, max_value=1)
  class Meta:
    model = Competence
    fields = (
      'id',
      'skill_id', 'specialist_id',
      'coefficient',
      'skill'
    )

class SpecialistSerializer(FlexFieldsModelSerializer):
  user = UserSerializer(
    read_only=True,
    omit=['specialist']
  )
  activities = SpecialtySerializer(
    source='specialty_set' , many=True, read_only=True,
    fields=['activity', 'is_main', 'id']
  )
  skills = CompetenceSerializer(
    source='competence_set', many=True, read_only=True,
    fields=['skill', 'coefficient', 'id']
  )

  is_active = serializers.BooleanField(required=False, read_only=True)

  username = serializers.CharField(required=False, write_only=True)
  password = serializers.CharField(required=False, write_only=True)
  is_staff = serializers.BooleanField(write_only=True)

  def create(self, validated_data):
    admin_group = Group.objects.get(name='education_admins')

    username = validated_data.pop('username', None)
    password = validated_data.pop('password', None)
    is_staff = validated_data.pop('is_staff', False)

    has_username = (not (username is None) and username)
    has_password = (not (password is None) and password)

    if has_username and has_password:
      user = User(username=username, is_staff=is_staff)
      user.set_password(password)
      user.save()
      if user.is_staff:
        user.groups.add(admin_group)

      specialist = Specialist(**validated_data)
      specialist.user = user
      specialist.save()
      return specialist
    else:
      raise serializers.ValidationError('Не указан username или password')

  def update(self, instance, validated_data):
    admin_group = Group.objects.get(name='education_admins')

    username = validated_data.pop('username', None)
    password = validated_data.pop('password', None)
    is_staff = validated_data.pop('is_staff', None)

    has_username = (not (username is None) and username)
    has_password = (not (password is None) and password)

    user = instance.user
    if not (user is None):
      if has_username:
        user.username = username
      if not is_staff is None:
        user.is_staff = is_staff
      if has_password:
        user.set_password(password)
      user.save()

      if user.is_staff:
        user.groups.add(admin_group)
      else:
        user.groups.remove(admin_group)

    elif has_username and has_password:
      if is_staff is None:
        is_staff = False
      user = User(username=username, is_staff=is_staff)
      user.set_password(password)
      user.save()
      if user.is_staff:
        user.groups.add(admin_group)
      instance.user = user

    instance.surname = validated_data.pop('surname', '')
    instance.name = validated_data.pop('name', '')
    instance.patronymic = validated_data.pop('patronymic', '')
    instance.role = validated_data.pop('role', '')
    instance.is_active = False if (user is None) else True
    instance.save()
    return instance

  class Meta:
    model = Specialist
    fields = (
      'id',
      'surname', 'name',
      'patronymic', 'role',
      'is_active',
      'skills', 'activities',
      'user',
      'username', 'password', 'is_staff',
      '__str__'
    )
    expandable_fields = {
      'activities': ActivitySerializer,
      'skills': SkillSerializer,
      'presence': PresenceSerializer,
    }

class FilteredDevelopment_directionListSerializer(serializers.ListSerializer):
  def to_representation(self, data):
    user=self.context['request'].user
    qs = Development_direction.objects.none()
    if user.is_staff:
      qs =  data
    else:
      if user.specialist is not None:
        qs = data.filter(skill__competence__specialist=user.specialist)

    return super(FilteredDevelopment_directionListSerializer, self).to_representation(qs)

class Development_directionSerializer(serializers.ModelSerializer):
  area_id = serializers.PrimaryKeyRelatedField(
    source='area', queryset=Educational_area.objects.all()
  )
  skills = SkillSerializer(
    source='skill_set', many=True, read_only=True
  )
  class Meta:
    model = Development_direction
    fields = (
      'id', 'area_id',
      'skills',
      'name', 'number',
    )
    list_serializer_class = FilteredDevelopment_directionListSerializer

class FilteredEducational_areaListSerializer(serializers.ListSerializer):
  def to_representation(self, data):
    user=self.context['request'].user
    qs = Educational_area.objects.none()
    if user.is_staff:
      qs = data
    else:
      if user.specialist is not None:
        qs = data.filter(development_direction__skill__competence__specialist=user.specialist)

    return super(FilteredEducational_areaListSerializer, self).to_representation(qs)

class Educational_areaSerializer(serializers.ModelSerializer):
  development_directions = Development_directionSerializer(
    source='development_direction_set', many=True, read_only=True,
  )
  class Meta:
    model = Educational_area
    fields = ('id', 'name', 'number', 'development_directions')
    list_serializer_class = FilteredEducational_areaListSerializer

class MethodSerializer(serializers.ModelSerializer):
  form_id = serializers.PrimaryKeyRelatedField(
    source='form', queryset=Form.objects.all()
  )
  def get_form_name(self, instance):
    return instance.form.name
  form_name = serializers.SerializerMethodField()
  class Meta:
    model = Method
    fields = (
      'id',
      'form_id', 'form_name',
      'name',
    )

class FormSerializer(serializers.ModelSerializer):
  methods = MethodSerializer(
    source='method_set', many=True, read_only=True
  )
  class Meta:
    model = Form
    fields = ('id', 'name', 'methods')

class Option_fileSerializer(serializers.ModelSerializer):
  option_id = serializers.PrimaryKeyRelatedField(
    source='option', queryset=Option.objects.all()
  )

  def get_name(self, instance):
    return os.path.split(instance.file.name)[-1]
  name = serializers.SerializerMethodField()
  class Meta:
    model = Option_file
    fields = (
      'id', 'option_id',
      'file',
      'name',
    )

class OptionSerializer(serializers.ModelSerializer):
  method_id = serializers.PrimaryKeyRelatedField(
    source='method', queryset=Method.objects.all(), required=False
  )
  method = MethodSerializer(
    read_only=True,
  )
  activity_id = serializers.PrimaryKeyRelatedField(
    source='activity', queryset=Activity.objects.all()
  )
  specialist_id = serializers.PrimaryKeyRelatedField(
    source='specialist', queryset=Specialist.objects.all(), required=False
  )
  option_files = Option_fileSerializer(
    source='option_file_set', many=True, read_only=True
  )
  skills = SkillSerializer(read_only=True, many=True)

  class Meta:
    model = Option
    fields = (
      'id', 'topic',
      'comment',
      'method_id', 'specialist_id',
      'activity_id', 'option_files',
      'skills',
      'method',
    )

class Job_fileSerializer(serializers.ModelSerializer):
  job_id = serializers.PrimaryKeyRelatedField(
    source='job', queryset=Job.objects.all()
  )

  def get_name(self, instance):
    return os.path.split(instance.file.name)[-1]
  name = serializers.SerializerMethodField()
  class Meta:
    model = Job_file
    fields = (
      'id', 'job_id',
      'file', 'name',
    )

class Skill_reportSerializer(FlexFieldsModelSerializer):
  job_id = serializers.PrimaryKeyRelatedField(
    source='job', queryset=Job.objects.all()
  )
  skill_id = serializers.PrimaryKeyRelatedField(
    source='skill', queryset=Skill.objects.all()
  )

  skill = SkillSerializer(read_only=True)

  class Meta:
    model = Skill_report
    fields = (
      'id',
      'job_id',
      'skill_id', 'skill',
      'mark',
    )

class JobSerializer(FlexFieldsModelSerializer):
  specialist_id = serializers.PrimaryKeyRelatedField(
    source='specialist', queryset=Specialist.objects.all(),
    required=False, write_only=True, allow_null=True
  )
  specialist = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role', '__str__']
  )
  activity_id = serializers.PrimaryKeyRelatedField(
    source='activity', queryset=Activity.objects.all(),
    write_only=True
  )
  activity = ActivitySerializer(
    read_only=True,
    fields=['id', 'name', 'color']
  )
  schedule_id = serializers.PrimaryKeyRelatedField(
    source='schedule', queryset=Schedule.objects.all().select_related('activity'),
    write_only=True, required=False, allow_null=True
  )
  schedule = ScheduleSerializer(
    read_only=True,
  )
  method_id = serializers.PrimaryKeyRelatedField(
    source='method', queryset=Method.objects.all(),
    write_only=True, required=False, allow_null=True
  )
  method = MethodSerializer(
    read_only=True,
  )

  reports = Skill_reportSerializer(
    source='skill_report_set',
    many=True, read_only=True,
  )
  job_files = Job_fileSerializer(
    source='job_file_set', many=True, read_only=True
  )

  def update(self, instance, validated_data):
    has_change_spec = False
    has_change_act = False

    if ('specialist' in validated_data):
      specialist = validated_data.get('specialist')
      has_change_spec = instance.specialist != specialist

    if ('activity' in validated_data):
      activity = validated_data.get('activity')
      has_change_act = instance.activity != activity

    if (has_change_spec) or (has_change_act):
      instance.clear_params()
      instance.save()

    return super(JobSerializer, self).update(instance, validated_data)


  class Meta:
    model = Job
    fields = (
      'id',
      'specialist_id', 'specialist',
      'activity_id', 'activity',
      'schedule_id', 'schedule',
      'reports',
      'job_files',
      'date', 'start_time',
      'comment', 'topic',
      'method_id', 'method',
      'report_comment',
    )

class Skill_reportSerializer(FlexFieldsModelSerializer):
  job_id = serializers.PrimaryKeyRelatedField(
    source='job', queryset=Job.objects.all()
  )
  skill_id = serializers.PrimaryKeyRelatedField(
    source='skill', queryset=Skill.objects.all()
  )

  job = JobSerializer(
    read_only=True,
    omit=['schedule', 'reports', 'job_files']
  )

  skill = SkillSerializer(read_only=True)

  class Meta:
    model = Skill_report
    fields = (
      'id',
      'job_id', 'job',
      'skill_id', 'skill',
      'mark',
    )