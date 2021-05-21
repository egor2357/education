from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from django.contrib.auth.models import User
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

class SkillSerializer(serializers.ModelSerializer):
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

class SpecialistSerializer(FlexFieldsModelSerializer):
  user_id = serializers.PrimaryKeyRelatedField(
    source='user', queryset=User.objects.all(), required=False
  )

  activities = ActivitySerializer(
    many=True, read_only=True,
    omit=['schedule', 'skills']
  )
  skills = SkillSerializer(
    many=True, read_only=True
  )
  presence = PresenceSerializer(
    source='presence_set', many=True, read_only=True
  )
  class Meta:
    model = Specialist
    fields = (
      'id',
      'surname', 'name',
      'patronymic', 'role',
      'skills', 'activities',
      'presence', 'user_id'
    )
    expandable_fields = {
      'activities': ActivitySerializer,
      'skills': SkillSerializer,
      'presence': PresenceSerializer,
    }

class UserSerializer(FlexFieldsModelSerializer):
  specialist = SpecialistSerializer(
    read_only=True,
    omit=['skills', 'activities', 'presence'],
  )
  class Meta:
    model = User
    fields = (
      'id', 'username',
      'is_staff', 'password',
      'specialist'
    )

  def create(self, validated_data):
    user = super().create(validated_data)
    user.set_password(validated_data['password'])
    user.save()
    return user

  def update(self, instance, validated_data):
    instance.username = validated_data['username']
    instance.set_password(validated_data['password'])
    instance.save()
    return instance

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

class CompetenceSerializer(serializers.ModelSerializer):
  skill_id = serializers.PrimaryKeyRelatedField(
    source='skill', queryset=Skill.objects.all()
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
    )

class SpecialtySerializer(serializers.ModelSerializer):
  activity_id = serializers.PrimaryKeyRelatedField(
    source='activity', queryset=Activity.objects.all()
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
    )