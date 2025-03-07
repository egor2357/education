import datetime
import os

from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer

from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

from education.models import (
  Exercise, Skill, Result, Development_direction,
  Activity, Schedule, Presence, Specialist, Specialty,
  Educational_area, Method, Form, Option_file, Option,
  Job_file, Job, Exercise_report, Job_report_file,
  Mission, Announcement, Notification, Appeal,
  Message, Task_group, Talent
)

#create your serializers here.

# /////////////////////////////////////////////////

class OnlyDateSerializer(serializers.Serializer):
  date = serializers.DateField(initial=datetime.date.today)

class JobByOptionSerializer(serializers.Serializer):
  option_id = serializers.IntegerField(max_value=None, min_value=1)

class GetAreasByDateSerializer(serializers.Serializer):
  by_date = serializers.DateField(default=datetime.date.today, required=False, label='Созданы до указанной даты')
  deleted = serializers.BooleanField(default=False, required=False, label='Удалены')

class GetAreasByIntervalSerializer(serializers.Serializer):
  start = serializers.DateField(label='Начало интервала')
  end = serializers.DateField(label='Окончание интервала')

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

class ExerciseSerializer(FlexFieldsModelSerializer):
  result_id = serializers.PrimaryKeyRelatedField(
    source='result', queryset=Result.objects.all()
  )

  result_number = serializers.IntegerField(source='result.number', read_only=True)
  skill_number = serializers.IntegerField(source='result.skill.number', read_only=True)
  direction_number = serializers.IntegerField(source='result.skill.direction.number', read_only=True)
  area_number = serializers.IntegerField(source='result.skill.direction.area.number', read_only=True)

  class Meta:
    model = Exercise
    fields = (
      'id',
      'name', 'number',
      'result_id',
      'skill_number',
      'result_number',
      'direction_number',
      'area_number',
    )

class ResultSerializer(FlexFieldsModelSerializer):
  exercises = ExerciseSerializer(many=True, read_only=True)

  skill_id = serializers.PrimaryKeyRelatedField(
    source='skill', queryset=Skill.objects.all()
  )

  skill_number = serializers.IntegerField(source='skill.number', read_only=True)
  direction_number = serializers.IntegerField(source='skill.direction.number', read_only=True)
  area_number = serializers.IntegerField(source='skill.direction.area.number', read_only=True)

  class Meta:
    model = Result
    fields = (
      'id',
      'name', 'number',
      'skill_id',
      'skill_number',
      'direction_number',
      'area_number',
      'exercises',
    )

class SkillSerializer(FlexFieldsModelSerializer):
  results = ResultSerializer(source='result_set', many=True, read_only=True)

  direction_id = serializers.PrimaryKeyRelatedField(
    source='direction', queryset=Development_direction.objects.all()
  )

  area_number = serializers.IntegerField(source='direction.area.number', read_only=True)
  direction_number = serializers.IntegerField(source='direction.number', read_only=True)

  class Meta:
    model = Skill
    fields = (
      'id',
      'name', 'number',
      'direction_id',
      'direction_number',
      'area_number',
      'results',
    )

class ActivitySerializer(FlexFieldsModelSerializer):
  class Meta:
    model = Activity
    fields = (
      'id',
      'name', 'color',
    )

class ScheduleSerializer(serializers.ModelSerializer):
  activity_id = serializers.PrimaryKeyRelatedField(
    source='activity', queryset=Activity.objects.all(),
    many=False, write_only=True
  )
  activity = ActivitySerializer(
    read_only=True,
  )
  class Meta:
    model = Schedule
    fields = (
      'id',
      'day', 'start_time',
      'activity_id', 'activity',
    )

class PresenceSummarySerializer(serializers.ModelSerializer):
  summary = serializers.CharField(allow_blank=True)

  class Meta:
    model = Presence
    fields = ('summary',)

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
  # summary = serializers.CharField(required=False)
  # Всегда берем summary от основного срока пребывания
  def get_summary(self, instance):
    return instance.main_interval.summary if instance.main_interval is not None else instance.summary

  summary = serializers.SerializerMethodField()

  def get_full_interval(self, instance):
    main_interval = instance.main_interval if instance.main_interval is not None else instance

    quarantine = main_interval.presence if hasattr(main_interval, 'presence') else None
    date_from = quarantine.date_from if quarantine is not None else main_interval.date_from
    date_to = main_interval.date_to
    quarantine_days = 0 if quarantine is None else (quarantine.date_to - quarantine.date_from).days + 1
    return {'date_from': date_from, 'date_to': date_to, 'quarantine_days': quarantine_days}
  full_interval = serializers.SerializerMethodField()

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

  class Meta:
    model = Presence
    fields = (
      'id',
      'specialist_id',
      'main_interval_id',
      'date_from', 'date_to',
      'is_available',
      'full_interval',
      'with_quarantine', 'quarantine_days',
      'summary'
    )

class UserSpecialistSerializer(FlexFieldsModelSerializer):
  activities_id = serializers.PrimaryKeyRelatedField(
    source='activities', many=True, queryset=Activity.objects.all()
  )
  exercises_id = serializers.PrimaryKeyRelatedField(
    source='exercises', many=True, read_only=True
  )

  class Meta:
    model = Specialist
    fields = (
      'id',
      'surname', 'name',
      'patronymic', 'role',
      'activities_id',
      'exercises_id',
      '__str__',
    )

class UserSerializer(FlexFieldsModelSerializer):
  specialist = UserSpecialistSerializer(read_only=True)
  class Meta:
    model = User
    fields = [
      'id',
      'username', 'is_staff',
      'specialist',
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

class SpecialistSerializer(FlexFieldsModelSerializer):
  user = UserSerializer(
    read_only=True,
    omit=['specialist']
  )
  activities = SpecialtySerializer(
    source='specialty_set' , many=True, read_only=True,
    fields=['activity', 'is_main', 'id']
  )

  exercises = serializers.PrimaryKeyRelatedField(read_only=True, many=True)

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
      serializer = UserSerializer(data={'username': username, 'is_staff': is_staff})
      if serializer.is_valid(raise_exception=True):
        user = serializer.save()

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

    new_data_dict = {}
    user = instance.user
    if not (user is None):
      if has_username:
        new_data_dict['username'] = username
      if not is_staff is None:
        new_data_dict['is_staff'] = is_staff
      serializer = UserSerializer(user, data=new_data_dict, partial=True)

    elif has_username:
      if is_staff is None:
        new_data_dict['is_staff'] = False
      new_data_dict['username'] = username
      serializer = UserSerializer(data=new_data_dict)

    if serializer.is_valid(raise_exception=True):
      user = serializer.save()

    if has_password:
      user.set_password(password)
      user.save()
      if user.is_staff:
        user.groups.add(admin_group)
      else:
        user.groups.remove(admin_group)

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
      'activities',
      'user',
      'username', 'password', 'is_staff',
      'exercises',
      '__str__'
    )
    expandable_fields = {
      'activities': ActivitySerializer,
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

class Educational_areaSerializer(FlexFieldsModelSerializer):
  development_directions = Development_directionSerializer(
    source='development_direction_set', many=True, read_only=True,
  )

  class Meta:
    model = Educational_area
    fields = ('id', 'name', 'number', 'development_directions')

class EducationalAreaOnlySerializer(FlexFieldsModelSerializer):
  class Meta:
    model = Educational_area
    fields = ('id', 'name', 'number')

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
      'file', 'thumbnail',
      'name',
    )

class OptionSerializer(serializers.ModelSerializer):
  activity_id = serializers.PrimaryKeyRelatedField(
    source='activity', queryset=Activity.objects.all()
  )
  specialist_id = serializers.PrimaryKeyRelatedField(
    source='specialist', queryset=Specialist.objects.all(), required=False
  )
  option_files = Option_fileSerializer(
    source='option_file_set', many=True, read_only=True
  )
  methods = MethodSerializer(read_only=True, many=True)
  exercises = ExerciseSerializer(read_only=True, many=True)
  date = serializers.DateField(read_only=True)

  class Meta:
    model = Option
    fields = (
      'id', 'topic',
      'comment',
      'specialist_id',
      'activity_id', 'option_files',
      'exercises', 'methods', 'date'
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
      'file', 'thumbnail',
      'name',
    )

class Job_report_fileSerializer(serializers.ModelSerializer):
  job_id = serializers.PrimaryKeyRelatedField(
    source='job', queryset=Job.objects.all()
  )

  def get_name(self, instance):
    return os.path.split(instance.file.name)[-1]
  name = serializers.SerializerMethodField()

  class Meta:
    model = Job_report_file
    fields = (
      'id', 'job_id',
      'file', 'thumbnail',
      'name',
    )


class Exercise_reportForJobSerializer(FlexFieldsModelSerializer):
  job_id = serializers.PrimaryKeyRelatedField(
    source='job', queryset=Job.objects.all()
  )
  exercise_id = serializers.PrimaryKeyRelatedField(
    source='exercise', queryset=Exercise.objects.all()
  )

  exercise = ExerciseSerializer(read_only=True)

  class Meta:
    model = Exercise_report
    fields = (
      'id',
      'job_id',
      'exercise_id', 'exercise',
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
  methods = MethodSerializer(read_only=True, many=True)
  reports = Exercise_reportForJobSerializer(
    source='exercise_report_set',
    many=True, read_only=True,
  )
  filled_reports_count = serializers.IntegerField(read_only=True)

  job_files = Job_fileSerializer(
    source='job_file_set', many=True, read_only=True
  )

  job_report_files = Job_report_fileSerializer(
    source='job_report_file_set', many=True, read_only=True
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
      'methods',
      'job_files', 'job_report_files',
      'date', 'start_time',
      'comment', 'topic',
      'report_comment',
      'filled_reports_count',
    )

class Exercise_reportSerializer(FlexFieldsModelSerializer):
  job_id = serializers.PrimaryKeyRelatedField(
    source='job', queryset=Job.objects.all()
  )
  exercise_id = serializers.PrimaryKeyRelatedField(
    source='exercise', queryset=Exercise.objects.all()
  )

  job = JobSerializer(
    read_only=True,
    omit=['schedule', 'reports', 'methods', 'job_files', 'job_report_files']
  )

  exercise = ExerciseSerializer(read_only=True)

  class Meta:
    model = Exercise_report
    fields = (
      'id',
      'job_id', 'job',
      'exercise_id', 'exercise',
      'mark',
    )

class MissionSerializer(FlexFieldsModelSerializer):
  executor_id = serializers.PrimaryKeyRelatedField(
    source='executor', queryset=Specialist.objects.all(),
    write_only=True, required=True, allow_null=False
  )
  controller_id = serializers.PrimaryKeyRelatedField(
    source='controller', queryset=Specialist.objects.all(),
    write_only=True, required=False, allow_null=True
  )

  director = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role', '__str__']
  )
  executor = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role', '__str__']
  )
  controller = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role', '__str__']
  )

  creation_date = serializers.DateTimeField(read_only=True)

  class Meta:
    model = Mission
    fields = '__all__'

class AnnouncementSerializer(FlexFieldsModelSerializer):
  creation_date = serializers.DateTimeField(read_only=True)

  class Meta:
    model = Announcement
    fields = '__all__'

class AppealSerializer(FlexFieldsModelSerializer):
  creator = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role', '__str__']
  )
  creation_date = serializers.DateTimeField(read_only=True)
  closed = serializers.BooleanField(read_only=True)
  count_unreaded = serializers.SerializerMethodField(read_only=True)

  def get_count_unreaded(self, obj):
    if ('request' in self.context):
      return Notification.objects\
      .filter(user_id=self.context['request'].user.id, type=1, meta__contains="{\"appeal_id\": %s}" % obj.id).count()
    else:
      return 0

  class Meta:
    model = Appeal
    fields = (
      'id',
      'creator',
      'creation_date', 'theme',
      'closed', 'count_unreaded'
    )

class AppealPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
  def get_queryset(self):
    request = self.context.get('request', None)
    queryset = super(AppealPrimaryKeyRelatedField, self).get_queryset()

    if not request or not queryset:
      return None

    if request.user.is_staff:
      qs = queryset.all()
    elif request.user.specialist is not None:
      qs = queryset.filter(creator=request.user.specialist)
    else:
      qs = queryset.none()

    return qs

class MessageSerializer(FlexFieldsModelSerializer):
  author = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role', '__str__']
  )
  appeal_id = AppealPrimaryKeyRelatedField(
    source='appeal', queryset=Appeal.objects,
  )
  creation_date = serializers.DateTimeField(read_only=True)
  reply = serializers.BooleanField(read_only=True)
  file = serializers.FileField(required=False)

  class Meta:
    model = Message
    fields = (
      'id',
      'author', 'appeal_id',
      'file',
      'creation_date',
      'text', 'reply',
      'filename'
    )

class Task_groupUserSerializer(FlexFieldsModelSerializer):
  author = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role', '__str__']
  )
  responsible = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role', '__str__']
  )

  creation_date = serializers.DateTimeField(read_only=True)
  anonymously = serializers.BooleanField(write_only=True, required=False, default=False)

  class Meta:
    model = Task_group
    fields = (
      'id',
      'author', 'responsible',
      'text', 'solution',
      'deadline', 'is_question',
      'creation_date',
      'anonymously',
    )
    read_only_fields = (
      'id',
      'author', 'responsible',
      'solution',
      'deadline',
      'creation_date',
    )

class Task_groupAdminSerializer(FlexFieldsModelSerializer):
  author = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role', '__str__']
  )
  responsible = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role', '__str__']
  )
  responsible_id = serializers.PrimaryKeyRelatedField(
    write_only=True, required=False, allow_null=True,
    source='responsible', queryset=Specialist.objects.all()
  )

  creation_date = serializers.DateTimeField(read_only=True)
  anonymously = serializers.BooleanField(write_only=True, required=False, default=False)

  class Meta:
    model = Task_group
    fields = (
      'id',
      'author',
      'text', 'solution',
      'responsible', 'responsible_id',
      'deadline', 'is_question',
      'creation_date',
      'anonymously',
    )

class TalentSerializer(FlexFieldsModelSerializer):
  specialist = SpecialistSerializer(
    read_only=True,
    fields=['id', 'surname', 'name', 'patronymic', 'role', '__str__']
  )
  area_id = serializers.PrimaryKeyRelatedField(
    write_only=True,
    source='area', queryset=Educational_area.objects.all()
  )
  area = Educational_areaSerializer(
    read_only=True, omit=['development_directions']
  )

  creation_date = serializers.DateTimeField(read_only=True)

  class Meta:
    model = Talent
    fields = (
      'id',
      'specialist',
      'area_id', 'area',
      'name', 'text',
      'creation_date'
    )


class NotificationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Notification
    fields = ('type', 'user')




# ------------------------ BY DATE SERIALIZERS -----------------------

class ByDateExerciseSerializer(FlexFieldsModelSerializer):
  result_id = serializers.PrimaryKeyRelatedField(
    source='result', queryset=Result.objects.all()
  )

  result_number = serializers.IntegerField(source='result.number', read_only=True)
  skill_number = serializers.IntegerField(source='result.skill.number', read_only=True)
  direction_number = serializers.IntegerField(source='result.skill.direction.number', read_only=True)
  area_number = serializers.IntegerField(source='result.skill.direction.area.number', read_only=True)
  def get_deleted(self, instance):
    by_date = self.context['by_date']
    if instance.lifetime and instance.lifetime.upper:
      return instance.lifetime.upper <= by_date
    else:
      return False
  deleted = serializers.SerializerMethodField(label='Было удалено', read_only=True)

  class Meta:
    model = Exercise
    fields = (
      'id',
      'name', 'number',
      'result_id',
      'skill_number',
      'result_number',
      'direction_number',
      'area_number',
      'deleted',
    )

class ByDateResultSerializer(FlexFieldsModelSerializer):
  exercises = ByDateExerciseSerializer(source='exercises_by_date', many=True, read_only=True)

  skill_id = serializers.PrimaryKeyRelatedField(
    source='skill', queryset=Skill.objects.all()
  )

  skill_number = serializers.IntegerField(source='skill.number', read_only=True)
  direction_number = serializers.IntegerField(source='skill.direction.number', read_only=True)
  area_number = serializers.IntegerField(source='skill.direction.area.number', read_only=True)
  def get_deleted(self, instance):
    by_date = self.context['by_date']
    if instance.lifetime and instance.lifetime.upper:
      return instance.lifetime.upper <= by_date
    else:
      return False
  deleted = serializers.SerializerMethodField(label='Было удалено', read_only=True)

  class Meta:
    model = Result
    fields = (
      'id',
      'name', 'number',
      'skill_id',
      'skill_number',
      'direction_number',
      'area_number',
      'exercises',
      'deleted',
    )

class ByDateSkillSerializer(FlexFieldsModelSerializer):
  results = ByDateResultSerializer(source='result_by_date', many=True, read_only=True)

  direction_id = serializers.PrimaryKeyRelatedField(
    source='direction', queryset=Development_direction.objects.all()
  )

  area_number = serializers.IntegerField(source='direction.area.number', read_only=True)
  direction_number = serializers.IntegerField(source='direction.number', read_only=True)
  def get_deleted(self, instance):
    by_date = self.context['by_date']
    if instance.lifetime and instance.lifetime.upper:
      return instance.lifetime.upper <= by_date
    else:
      return False
  deleted = serializers.SerializerMethodField(label='Было удалено', read_only=True)

  class Meta:
    model = Skill
    fields = (
      'id',
      'name', 'number',
      'direction_id',
      'direction_number',
      'area_number',
      'results',
      'deleted',
    )

class ByDateDevelopment_directionSerializer(serializers.ModelSerializer):
  area_id = serializers.PrimaryKeyRelatedField(
    source='area', queryset=Educational_area.objects.all()
  )
  skills = ByDateSkillSerializer(
    source='skill_by_date', many=True, read_only=True
  )
  def get_deleted(self, instance):
    by_date = self.context['by_date']
    if instance.lifetime and instance.lifetime.upper:
      return instance.lifetime.upper <= by_date
    else:
      return False
  deleted = serializers.SerializerMethodField(label='Было удалено', read_only=True)

  class Meta:
    model = Development_direction
    fields = (
      'id', 'area_id',
      'skills',
      'name', 'number',
      'deleted',
    )

class ByDateEducational_areaSerializer(FlexFieldsModelSerializer):
  development_directions = ByDateDevelopment_directionSerializer(
    source='development_direction_by_date', many=True, read_only=True,
  )
  def get_deleted(self, instance):
    by_date = self.context['by_date']
    if instance.lifetime and instance.lifetime.upper:
      return instance.lifetime.upper <= by_date
    else:
      return False
  deleted = serializers.SerializerMethodField(label='Было удалено', read_only=True)

  class Meta:
    model = Educational_area
    fields = (
      'id', 'name', 'number', 'development_directions',
      'deleted',
    )
