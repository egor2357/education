import json
from .models import *
from .utils import (loop, send_message)
from django.conf import settings

def option_update_related(option, request):
  #Требует FormData для передачи файлов
  if 'files_id' in request.data:
    files_id = json.loads(request.data['files_id'])

    files_to_save = []
    files = request.FILES.getlist('files')
    for file in files:
      file_data = file
      new_file = Option_file(option=option, file=file_data)
      new_file.create_thumbnail()
      files_to_save.append(new_file)

    option.option_file_set.exclude(pk__in=files_id).delete()
    Option_file.objects.bulk_create(files_to_save)

  if 'exercises' in request.data:
    exercises = json.loads(request.data['exercises'])
    exercises = Exercise.objects.filter(pk__in=exercises)
    option.exercises.clear()
    option.exercises.set(exercises)

  if 'methods' in request.data:
    methods = json.loads(request.data['methods'])
    methods = Method.objects.filter(pk__in=methods)
    option.methods.set(methods)

def job_update_related(job, request):
  if 'files_id' in request.data:
    files_id = json.loads(request.data['files_id'])

    files_to_save = []
    files = request.FILES.getlist('files')
    for file in files:
      new_file = Job_file(job=job, file=file)
      new_file.create_thumbnail()
      files_to_save.append(new_file)

    job.job_file_set.exclude(pk__in=files_id).delete()
    Job_file.objects.bulk_create(files_to_save)

  if 'report_files_id' in request.data:
    report_files_id = json.loads(request.data['report_files_id'])

    report_files_to_save = []
    report_files = request.FILES.getlist('report_files')
    for report_file in report_files:
      new_report_file = Job_report_file(job=job, file=report_file)
      new_report_file.create_thumbnail()
      report_files_to_save.append(new_report_file)

    job.job_report_file_set.exclude(pk__in=report_files_id).delete()
    Job_report_file.objects.bulk_create(report_files_to_save)

  if 'option_files' in request.data:
    option_files = json.loads(request.data['option_files'])
    option_files_ids = [option_file['uid'] for option_file in option_files]
    option_files_qs = Option_file.objects.filter(pk__in=option_files_ids)

    option_files_to_save = []
    for option_file in option_files_qs:

      data_obj = ContentFile(option_file.file.read())
      name = os.path.split(option_file.file.name)[-1]
      data_obj.name = name
      new_file = Job_file(job=job, file=data_obj)
      new_file.create_thumbnail()
      option_files_to_save.append(new_file)

    Job_file.objects.bulk_create(option_files_to_save)

  if 'reports' in request.data:
    exercises = json.loads(request.data['reports'])

    curr_exercise_reports_ids = list(job.exercise_report_set.all().values_list('exercise_id', flat=True))

    exercises_to_save = []
    remaining_exercises = []

    for exercise_id in exercises:
      if exercise_id not in curr_exercise_reports_ids:
        exercises_to_save.append(
          Exercise_report(job=job, exercise_id=exercise_id)
        )
      else:
        remaining_exercises.append(exercise_id)

    exercise_reports_qs = job.exercise_report_set.all()
    exercise_reports_qs.exclude(exercise_id__in=remaining_exercises).delete()
    Exercise_report.objects.bulk_create(exercises_to_save)

  if 'methods' in request.data:
    methods = json.loads(request.data['methods'])
    methods = Method.objects.filter(pk__in=methods)
    job.methods.set(methods)

  if 'marks' in request.data:
    marks = request.data.get('marks', [])
    for mark in marks:
      exercise_report = Exercise_report.objects.get(pk=mark['id'])
      exercise_report.mark = mark['mark']
      exercise_report.save()

def check_presence_clashes(specialist, date_from, date_to, exclude_presence=None):
  spec_presense_qs = Presence.objects.filter(specialist=specialist)
  if exclude_presence is not None:
    spec_presense_qs = spec_presense_qs.exclude(exclude_presence)
  clashes_qs = spec_presense_qs.exclude(date_to__lt=date_from)
  clashes_qs = clashes_qs.exclude(date_from__gt=date_to)

  if clashes_qs.exists():
    raise ValidationError(
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


def send_messages_after_list_mission(new_missions):
  try:
    users = list(set(
      list(new_missions.exclude(director=None).values_list('director__user_id', flat=True)) +
      list(new_missions.exclude(controller=None).values_list('controller__user_id', flat=True)) +
      list(User.objects.filter(is_staff=True).values_list('id', flat=True))
    ))
    loop.run_until_complete(send_message({
      'action': 'missions.update',
      'type': 'list',
      'list_idx': users
    }, settings.WS_IP))
  except:
    pass


def send_messages_after_create_mission(serializer):
  try:
    users = []
    if (serializer.instance.executor):
      Notification.objects.create(user_id=serializer.instance.executor.user_id, type=0,
                                  meta=json.dumps({'mission_id': serializer.instance.id}))
      users.append(serializer.instance.executor.user_id)
    if (serializer.instance.controller and serializer.instance.executor != serializer.instance.controller):
      Notification.objects.create(user_id=serializer.instance.controller.user_id, type=0,
                                  meta=json.dumps({'mission_id': serializer.instance.id}))
      users.append(serializer.instance.controller.user_id)
    loop.run_until_complete(send_message({'action': 'notifications.update.0', 'type': 'list',
                                          'list_idx': users}, settings.WS_IP))
    admins = list(User.objects.filter(is_staff=True).values_list('id', flat=True))
    loop.run_until_complete(send_message({'action': 'missions.update', 'type': 'list',
                                          'list_idx': admins}, settings.WS_IP))
  except:
    pass

def send_messages_after_update_mission(serializer):
  try:
    users = list(User.objects.filter(is_staff=True).values_list('id', flat=True))
    if (serializer.instance.executor and serializer.instance.executor.user_id not in users):
      users.append(serializer.instance.executor.user_id)
    if (serializer.instance.controller and serializer.instance.executor != serializer.instance.controller
            and serializer.instance.controller.user_id not in users):
      users.append(serializer.instance.controller.user_id)
    loop.run_until_complete(send_message({'action': 'missions.update', 'type': 'list',
                                          'list_idx': users}, settings.WS_IP))
  except:
    pass

def send_messages_after_delete_mission(instance):
  try:
    users = list(User.objects.filter(is_staff=True).values_list('id', flat=True))
    if (instance.controller and instance.controller.user_id not in users):
      users.append(instance.controller.user_id)
    if (instance.executor and instance.executor.user_id not in users):
      users.append(instance.executor.user_id)
    loop.run_until_complete(send_message({'action': 'missions.update', 'type': 'list',
                                          'list_idx': users}, settings.WS_IP))
  except:
    pass

def send_messages_after_execute_mission(mission, user):
  try:
    users = list(User.objects.filter(is_staff=True).values_list('id', flat=True))
    if (mission.executor and mission.executor.user_id not in users):
      users.append(mission.executor.user_id)
    if (mission.director
            and mission.controller
            and user.id == mission.controller.user_id
            and mission.director.user_id not in users):
      users.append(mission.director.user_id)
    if (mission.director
            and mission.controller
            and user.id == mission.director.user_id
            and mission.controller.user_id not in users):
      users.append(mission.controller.user_id)
    loop.run_until_complete(send_message({'action': 'missions.update', 'type': 'list',
                                          'list_idx': users}, settings.WS_IP))
  except:
    pass

def send_messages_after_create_announcement(request, serializer):
  try:
    users = User.objects.exclude(id=request.user.id).values_list('id', flat=True)
    for user in users:
      Notification.objects.create(user_id=user, type=2, meta=json.dumps({'announcement_id': serializer.instance.id}))
    loop.run_until_complete(send_message({'action': 'notifications.update.2', 'type': 'exclude',
                                          'exclude_id': request.user.id}, settings.WS_IP))
  except:
    pass

def send_messages_after_update_announcement(request):
  try:
    users = User.objects.exclude(id=request.user.id).values_list('id', flat=True)
    loop.run_until_complete(send_message({'action': 'announcements.update', 'type': 'exclude',
                                          'exclude_id': request.user.id}, settings.WS_IP))
  except:
    pass

def send_messages_after_delete_announcement(request):
  try:
    users = User.objects.exclude(id=request.user.id).values_list('id', flat=True)
    loop.run_until_complete(send_message({'action': 'announcements.update', 'type': 'exclude',
                                          'exclude_id': request.user.id}, settings.WS_IP))
  except:
    pass

def send_messages_after_create_appeal():
  try:
    admins = list(User.objects.filter(is_staff=True).values_list('id', flat=True))
    loop.run_until_complete(send_message({'action': 'appeals.update', 'type': 'list',
                                        'list_idx': admins}, settings.WS_IP))
  except:
    pass

def send_messages_after_delete_appeal(instance):
  try:
    admins = list(User.objects.filter(is_staff=True).values_list('id', flat=True))
    if (instance.creator.user_id not in admins):
      admins.append(instance.creator.user_id)
    loop.run_until_complete(send_message({'action': 'appeals.update', 'type': 'list',
                                          'list_idx': admins}, settings.WS_IP))
  except:
    pass

def send_messages_after_close_appeal(appeal):
  try:
    admins = list(User.objects.filter(is_staff=True).values_list('id', flat=True))
    if (appeal.creator.user_id not in admins):
      admins.append(appeal.creator.user_id)
    loop.run_until_complete(send_message({'action': 'appeals.update', 'type': 'list',
                                          'list_idx': admins}, settings.WS_IP))
  except:
    pass