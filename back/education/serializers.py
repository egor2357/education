from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

from .models import *

import datetime

#create your serializers here.

# /////////////////////////////////////////////////

class OnlyDateSerializer(serializers.Serializer):
  date = serializers.DateField(initial=datetime.date.today)

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

class SkillSerializer(FlexFieldsModelSerializer):
  direction_id = serializers.PrimaryKeyRelatedField(
    source='direction', queryset=Development_direction.objects.all()
  )
  class Meta:
    model = Skill
    fields = ('id', 'name', 'number', 'direction_id')

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
  date_from = serializers.DateField()
  date_to = serializers.DateField()

  def validate(self, data):
    if data['date_to'] < data['date_from']:
      raise serializers.ValidationError('Дата начала должна быть меньше или равна дате конца')
    return data

  class Meta:
    model = Presence
    fields = (
      'id', 'specialist_id',
      'date_from', 'date_to',
      'is_available'
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
  presence = PresenceSerializer(
    source='presence_set', many=True, read_only=True
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
      'presence',
      'user',
      'username', 'password', 'is_staff'
    )
    expandable_fields = {
      'activities': ActivitySerializer,
      'skills': SkillSerializer,
      'presence': PresenceSerializer,
    }

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

class Educational_areaSerializer(serializers.ModelSerializer):
  development_directions = Development_directionSerializer(
    source='development_direction_set', many=True, read_only=True
  )
  class Meta:
    model = Educational_area
    fields = ('id', 'name', 'number', 'development_directions')

class MethodSerializer(serializers.ModelSerializer):
  form_id = serializers.PrimaryKeyRelatedField(
    source='form', queryset=Form.objects.all()
  )
  class Meta:
    model = Method
    fields = (
      'id', 'form_id',
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
  class Meta:
    model = Option_file
    fields = (
      'id', 'option_id',
      'file',
    )

class OptionSerializer(serializers.ModelSerializer):
  method_id = serializers.PrimaryKeyRelatedField(
    source='method', queryset=Method.objects.all(), required=False
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
  class Meta:
    model = Option
    fields = (
      'id', 'caption',
      'method_id', 'specialist_id',
      'activity_id', 'option_files'
    )

class Job_fileSerializer(serializers.ModelSerializer):
  job_id = serializers.PrimaryKeyRelatedField(
    source='job', queryset=Job.objects.all()
  )
  class Meta:
    model = Job_file
    fields = (
      'id', 'job_id',
      'file'
    )

class Skill_reportSerializer(serializers.ModelSerializer):
  job_id = serializers.PrimaryKeyRelatedField(
    source='job', queryset=Job.objects.all()
  )
  skill_id = serializers.PrimaryKeyRelatedField(
    source='skill', queryset=Skill.objects.all()
  )
  class Meta:
    model = Skill_report
    fields = (
      'id', 'job_id', 'skill_id',
      'mark', 'comment'
    )

class JobSerializer(FlexFieldsModelSerializer):
  specialist_id = serializers.PrimaryKeyRelatedField(
    source='specialist', queryset=Specialist.objects.all(),
    required=False, write_only=True
  )
  specialist = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role']
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
    source='schedule', queryset=Schedule.objects.all(),
    write_only=True
  )
  schedule = ScheduleSerializer(
    read_only=True,
  )

  reports = Skill_reportSerializer(
    many=True, read_only=True
  )
  job_files = Job_fileSerializer(
    source='job_file_set', many=True, read_only=True
  )
  class Meta:
    model = Job
    fields = (
      'id',
      'specialist_id', 'specialist',
      'activity_id', 'activity',
      'schedule_id', 'schedule',
      'reports',
      'job_files',
      'date', 'start_time', 'comment',
    )