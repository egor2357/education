from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate
from .models import *

#create your serializers here.
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

class ScheduleSerializer(serializers.ModelSerializer):
  activity_id = serializers.PrimaryKeyRelatedField(
    source='activity', queryset=Activity.objects.all()
  )
  class Meta:
    model = Schedule
    fields = ('id', 'day', 'start_time', 'activity_id')

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
  schedule = ScheduleSerializer(
    source='schedule_set', many=True, read_only=True
  )
  class Meta:
    model = Activity
    fields = ('id', 'name', 'color', 'skills', 'schedule')
    expandable_fields = {
      'skills': SkillSerializer,
      'schedule': ScheduleSerializer,
    }

class PresenceSerializer(serializers.ModelSerializer):
  specialist_id = serializers.PrimaryKeyRelatedField(
    source='specialist', queryset=Specialist.objects.all()
  )
  class Meta:
    model = Presence
    fields = (
      'id', 'specialist_id',
      'date_from', 'date_to',
      'is_available'
    )

class UserSerializer(FlexFieldsModelSerializer):
  def to_representation(self, instance):
    obj = {
      'id': instance.id,
      'username': instance.username,
      'is_staff': instance.is_staff,
      'specialist': None
    }
    if hasattr(instance, 'specialist'):
      obj['specialist'] = {
        'id': instance.specialist.id,
        'surname': instance.specialist.surname,
        'name': instance.specialist.name,
        'patronymic': instance.specialist.patronymic,
        'role': instance.specialist.role
      }
    return obj
  class Meta:
    model = User
    fields = '__all__'

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
  user = UserSerializer(read_only=True)
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

    username = validated_data.pop('username', '')
    password = validated_data.pop('password', '')
    is_staff = validated_data.pop('is_staff', False)

    if username and password:
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

    username = validated_data.pop('username', '')
    password = validated_data.pop('password', '')
    is_staff = validated_data.pop('is_staff', None)

    user = instance.user
    if not (user is None):
      if username:
        user.username = username
      if not is_staff is None:
        user.is_staff = is_staff
      if password:
        user.set_password(password)
      user.save()

      if user.is_staff:
        user.groups.add(admin_group)
      else:
        user.groups.remove(admin_group)

    elif username and password:
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

class JobSerializer(serializers.ModelSerializer):
  option_id = serializers.PrimaryKeyRelatedField(
    source='option', queryset=Option.objects.all(), required=False
  )
  specialist_id = serializers.PrimaryKeyRelatedField(
    source='specialist', queryset=Specialist.objects.all(), required=False
  )
  activity_id = serializers.PrimaryKeyRelatedField(
    source='activity', queryset=Activity.objects.all()
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
      'reports','job_files',
      'option_id', 'specialist_id',
      'activity_id',
      'date', 'start_time', 'comment'
    )