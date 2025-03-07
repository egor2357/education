import json

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from django.core.files.base import ContentFile
from django.contrib.postgres.fields import JSONField, DateRangeField
from django.conf import settings
from .utils import send_message, loop

import datetime

import os

from PIL import Image
from io import BytesIO

from django.db.models import Transform

class UpperInc(Transform):
    lookup_name = "upper_inc"
    function = "UPPER_INC"
DateRangeField.register_lookup(UpperInc)
class UpperInf(Transform):
  lookup_name = "upper_inf"
  function = "UPPER_INF"
DateRangeField.register_lookup(UpperInf)
class LowerInc(Transform):
  lookup_name = "lower_inc"
  function = "LOWER_INC"
DateRangeField.register_lookup(LowerInc)
class LowerInf(Transform):
  lookup_name = "lower_inf"
  function = "LOWER_INF"
DateRangeField.register_lookup(LowerInf)
class DateRangeLower(Transform):
  lookup_name = "lower"
  function = "LOWER"
DateRangeField.register_lookup(DateRangeLower)
class DateRangeUpper(Transform):
  lookup_name = "upper"
  function = "UPPER"
DateRangeField.register_lookup(DateRangeUpper)

class Educational_area(models.Model):
  name = models.TextField(unique=True, verbose_name='Название')
  number = models.PositiveSmallIntegerField(verbose_name='Номер')
  lifetime = DateRangeField(verbose_name='Время жизни')

  class Meta:
    db_table = 'educational_area'
    verbose_name = 'Образовательная область'
    verbose_name_plural = 'Образовательные области'
    ordering = ['number']

  def __str__(self):
    return self.name


class Development_direction(models.Model):
  area = models.ForeignKey(
    Educational_area, null=False,
    on_delete=models.CASCADE, verbose_name='Образовательная область'
  )

  name = models.TextField(verbose_name='Название')
  number = models.PositiveSmallIntegerField(verbose_name='Номер')
  lifetime = DateRangeField(verbose_name='Время жизни')

  class Meta:
    db_table = 'development_direction'
    verbose_name = 'Направление развития'
    verbose_name_plural = 'Направления развития'
    ordering = ['area', 'number']
    unique_together = ('area', 'name',)

  def __str__(self):
    return self.name

class Skill(models.Model):
  direction = models.ForeignKey(
    Development_direction, null=False,
    on_delete=models.CASCADE, verbose_name='Направление развития'
  )

  name = models.TextField(verbose_name='Название')
  number = models.PositiveSmallIntegerField(verbose_name='Номер')
  lifetime = DateRangeField(verbose_name='Время жизни')

  class Meta:
    db_table = 'skill'
    verbose_name = 'Навык'
    verbose_name_plural = 'Навыки'
    ordering = ['direction', 'number']
    unique_together = ('direction', 'name',)

  def __str__(self):
    return self.name

class Result(models.Model):
  skill = models.ForeignKey(
    Skill, null=False,
    on_delete=models.CASCADE, verbose_name='Навык'
  )

  name = models.TextField(verbose_name='Название')
  number = models.PositiveSmallIntegerField(verbose_name='Номер')
  lifetime = DateRangeField(verbose_name='Время жизни')

  class Meta:
    db_table = 'result'
    verbose_name = 'Ожидаемый результат'
    verbose_name_plural = 'Ожидаемые результаты'
    ordering = ['skill', 'number']
    unique_together = ('skill', 'name',)

  def __str__(self):
    return self.name

class Exercise(models.Model):
  result = models.ForeignKey(
    Result, null=False, related_name='exercises',
    on_delete=models.CASCADE, verbose_name='Ожидаемый результат'
  )

  name = models.TextField(verbose_name='Название')
  number = models.PositiveSmallIntegerField(verbose_name='Номер')
  lifetime = DateRangeField(verbose_name='Время жизни')

  class Meta:
    db_table = 'exercise'
    verbose_name = 'Упражнение'
    verbose_name_plural = 'Упражнения'
    ordering = ['result', 'number']
    unique_together = ('result', 'name',)

  def __str__(self):
    return self.name

class Exercise_to_specialist(models.Model):
  exercise = models.ForeignKey(
    Exercise, null=False,
    on_delete=models.CASCADE, verbose_name='Упражнение'
  )
  specialist = models.ForeignKey(
    'Specialist', null=False,
    on_delete=models.CASCADE, verbose_name='Специалист'
  )

  class Meta:
    db_table = 'exercise_to_specialist'
    verbose_name = 'Упражнение для специалиста'
    verbose_name_plural = 'Упражнения для специалистов'
    unique_together = ('specialist', 'exercise')


class Specialist(models.Model):
  user = models.OneToOneField(
    User, null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Пользователь'
  )

  activities = models.ManyToManyField('Activity', through='Specialty', verbose_name='Направления деятельности')
  exercises = models.ManyToManyField(
    Exercise, related_name='specialists',
    through='Exercise_to_specialist', verbose_name='Разрешенные упражнения'
  )

  surname = models.CharField(max_length=50, blank=True, default='', verbose_name='Фамилия')
  name = models.CharField(max_length=50, blank=True, default='', verbose_name='Имя')
  patronymic = models.CharField(max_length=50, blank=True, default='', verbose_name='Отчество')
  role = models.TextField(max_length=200, blank=True, verbose_name='Роль')
  is_active = models.BooleanField(default=True, verbose_name='Активен ли')

  @classmethod
  def get_available(self, activity, date):
    available_specs = activity.specialty_set.values_list('specialist_id', 'is_main')
    available_specs_list = list(available_specs)
    all_specs_ids = [spec[0] for spec in available_specs_list]
    main_specs_ids = [spec[0] for spec in available_specs_list if spec[1]]
    add_specs_ids = [spec[0] for spec in available_specs_list if not spec[1]]

    presense_specs_ids = Presence.objects.filter(
      specialist_id__in=all_specs_ids,
      date_from__lte=date,
      date_to__gte=date,
      is_available=True
    ).values_list('specialist_id', flat=True)

    specialists = Specialist.objects.filter(pk__in=presense_specs_ids)

    if specialists.filter(pk__in=main_specs_ids).exists():
      specialist = specialists.filter(pk__in=main_specs_ids).first()
    elif specialists.filter(pk__in=add_specs_ids).exists():
      specialist = specialists.filter(pk__in=add_specs_ids).first()
    else:
      specialist = None

    return specialist

  @classmethod
  def set_to_period(self, date_from, date_to):
    today = datetime.date.today()
    if date_from <= today:
      date_from = today + datetime.timedelta(days=1)
    jobs = Job.objects.filter(
      date__gte=date_from,
      date__lte=date_to,
      specialist=None,
    )

    for job in jobs:
      specialist = self.get_available(job.activity, job.date)
      job.specialist=specialist
      job.clear_params()
      job.save()

  class Meta:
    db_table = 'specialist'
    verbose_name = 'Специалист'
    verbose_name_plural = 'Специалисты'
    ordering = ['surname']

  def __str__(self):
    res = ''
    if (self.surname):
      res += self.surname
      if self.name:
        res += ' {0}.'.format(self.name[0])
      if self.patronymic:
        res += ' {0}.'.format(self.patronymic[0])
    elif self.user:
      res = self.user.login
    else:
      res = '{0} {1} {2}'.format(self.surname, self.name, self.patronymic)

    return res

class Presence(models.Model):
  specialist = models.ForeignKey(
    Specialist, null=False,
    on_delete=models.CASCADE, verbose_name='Специалист'
  )
  main_interval = models.OneToOneField(
    'self', null=True, default=None,
    on_delete=models.CASCADE, verbose_name='Основной период'
  )

  date_from = models.DateField(verbose_name='Первый день')
  date_to = models.DateField(verbose_name='Последний день')
  is_available = models.BooleanField(default=True, verbose_name='Является ли доступным')
  summary = models.TextField(default='', blank=True, verbose_name='Отчет по пребыванию')

  def clear_jobs(self):
    presence = self
    if presence.main_interval != None:
      presence = presence.main_interval

    date_from = presence.date_from
    today = datetime.date.today()
    if date_from <= today:
      date_from = today + datetime.timedelta(days=1)

    affected_jobs = Job.objects.filter(
      date__gte=date_from,
      date__lte=presence.date_to,
      specialist=presence.specialist
    )
    for job in affected_jobs:
      job.specialist = None
      job.clear_params()
      job.save()

  def set_jobs(self):
    presence = self
    if presence.main_interval != None:
      presence = presence.main_interval

    date_from = presence.date_from
    today = datetime.date.today()
    if date_from <= today:
      date_from = today + datetime.timedelta(days=1)

    affected_jobs = Job.objects.filter(
      date__gte=date_from,
      date__lte=presence.date_to,
      activity__in=presence.specialist.activities.all(),
      specialist=None
    )
    for job in affected_jobs:
      job.specialist = presence.specialist
      job.clear_params()
      job.save()

  class Meta:
    db_table = 'presence'
    verbose_name = 'Присутствие'
    verbose_name_plural = 'Присутствия'
    ordering = ['date_from']

  def __str__(self):
    return '{0} с {1} по {2}'.format(
      self.specialist,
      self.date_from.strftime('%m.%d'),
      self.date_to.strftime('%m.%d')
    )

class Form(models.Model):
  name = models.TextField(unique=True, verbose_name='Название')

  class Meta:
    db_table = 'form'
    verbose_name = 'Методы проведения занятий'
    verbose_name_plural = 'Методы проведения занятий'
    ordering = ['name']

  def __str__(self):
    return self.name

class Method(models.Model):
  form = models.ForeignKey(
    Form, null=False,
    on_delete=models.CASCADE, verbose_name='Методы'
  )

  name = models.TextField(verbose_name='Название')

  class Meta:
    db_table = 'method'
    verbose_name = 'Форма проведения занятия'
    verbose_name_plural = 'Формы проведения занятия'
    ordering = ['name']
    unique_together = ('form', 'name')

  def __str__(self):
    return self.name

class Activity(models.Model):
  name = models.TextField(unique=True, verbose_name='Название')
  color = models.CharField(max_length=7, default='#CCCCCC', blank=True, verbose_name='Код цвета')

  class Meta:
    db_table = 'activity'
    verbose_name = 'Вид деятельности'
    verbose_name_plural = 'Виды деятельности'
    ordering = ['name']

  def __str__(self):
    return self.name

class Schedule(models.Model):
  weekday_names = [
    'Понедельник', 'Вторник',
    'Среда', 'Четверг',
    'Пятница', 'Суббота', 'Воскресенье'
  ]
  day_choices = [item for item in enumerate(weekday_names)]

  activity = models.ForeignKey(
    Activity, null=False,
    on_delete=models.CASCADE, verbose_name='Вид деятельности'
  )

  day = models.PositiveSmallIntegerField(choices=day_choices, verbose_name='Индекс дня недели')
  start_time = models.TimeField(verbose_name='Время начала')

  class Meta:
    db_table = 'schedule'
    verbose_name = 'Шаблон занятия'
    verbose_name_plural = 'Шаблоны занятия'
    ordering = ['day', 'start_time']

  def __str__(self):
    return '{0}: {1} - {2}'.format(
      self.weekday_names[self.day],
      self.start_time.strftime('%H:%M'),
      self.activity.name
    )

class Specialty(models.Model):
  specialist = models.ForeignKey(
    Specialist,
    on_delete=models.CASCADE, verbose_name='Специалист'
  )
  activity = models.ForeignKey(
    Activity,
    on_delete=models.CASCADE, verbose_name='Вид деятельности'
  )

  is_main = models.BooleanField(default=True, verbose_name='Является ли основным')

  def reset_jobs(self):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    jobs = Job.objects.filter(
      date__gte=tomorrow,
      specialist=self.specialist,
      activity=self.activity,
    )
    for job in jobs:
      specialist = Specialist.get_available(job.activity, job.date)
      job.specialist = specialist
      job.clear_params()
      job.save()

  def fill_jobs(self):
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    jobs = Job.objects.filter(
      date__gte=tomorrow,
      specialist=None,
      activity=self.activity,
    )
    for job in jobs:
      specialist = Specialist.get_available(job.activity, job.date)
      job.specialist=specialist
      job.clear_params()
      job.save()


  class Meta:
    db_table = 'specialty'
    verbose_name = 'Направление деятельности специалиста'
    verbose_name_plural = 'Направления деятельности специалиста'
    unique_together = ('specialist', 'activity')
    ordering = ['specialist', 'activity']

  def __str__(self):
    return '{0} ответственен за {1}'.format(
      self.specialist,
      self.activity
    )

class Exercise_to_option(models.Model):
  exercise = models.ForeignKey(
    Exercise, null=False,
    on_delete=models.CASCADE, verbose_name='Упражнение'
  )
  option = models.ForeignKey(
    'Option', null=False,
    on_delete=models.CASCADE, verbose_name='Вариант занятия'
  )

  class Meta:
    db_table = 'option_exercises'
    verbose_name = 'Упражнение в шаблоне занятия'
    verbose_name_plural = 'Упражнения в шаблонах занятий'
    unique_together = ('exercise', 'option')

class Option(models.Model):
  specialist = models.ForeignKey(
    Specialist, null=True,
    on_delete=models.SET_NULL, verbose_name='Специалист'
  )
  activity = models.ForeignKey(
    Activity, null=False,
    on_delete=models.CASCADE, verbose_name='Вид деятельсности')

  methods = models.ManyToManyField(Method, verbose_name='Формы')
  exercises = models.ManyToManyField(
    Exercise, through=Exercise_to_option,
    verbose_name='Выполняемые на занятии упражнения'
  )

  topic = models.TextField(verbose_name='Тема занятия')
  comment = models.TextField(blank=True, verbose_name='Комментарий по занятию')

  date = models.DateField(null=False, blank=True, auto_now_add=True, verbose_name='Дата добавления')

  class Meta:
    db_table = 'option'
    verbose_name = 'Вариант занятия'
    verbose_name_plural = 'Варианты занятия'
    ordering = ['specialist']

  def __str__(self):
    return '{0} ({1}, {2})'.format(
      self.topic,
      self.specialist,
      self.activity
    )

class Option_file(models.Model):
  def get_file_upload_to(instance, filename):
    return 'option_files/{0}/{1}/{2}'.format(
      instance.option.activity.name,
      instance.option.topic,
      filename
    )

  def get_thumbnail_upload_to(instance, filename):
    return 'option_files/{0}/{1}/thumbnail_{2}'.format(
      instance.option.activity.name,
      instance.option.topic,
      filename
    )

  option = models.ForeignKey(
    Option, null=False,
    on_delete=models.CASCADE, verbose_name='Вариант занятия'
  )

  file = models.FileField(
    upload_to=get_file_upload_to,
    max_length=255,
    verbose_name='Файл'
  )

  thumbnail = models.ImageField(
    null=True,
    default=None,
    upload_to=get_thumbnail_upload_to,
    max_length=255,
    verbose_name='Миниатюра'
  )

  class Meta:
    db_table = 'option_file'
    verbose_name = 'Файл варианта занятия'
    verbose_name_plural = 'Файлы варианта занятия'
    ordering = ['option']

  def __str__(self):
    return self.file.name

  def create_thumbnail(self):
    try:
      file_name, file_extension = os.path.splitext(self.file.name)

      if file_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
      elif file_extension == '.gif':
        FTYPE = 'GIF'
      elif file_extension == '.png':
        FTYPE = 'PNG'
      else:
        return

      image = Image.open(self.file)
      image.thumbnail((200,200), Image.ANTIALIAS)

      temp_thumb = BytesIO()
      image.save(temp_thumb, FTYPE)
      temp_thumb.seek(0)

      data_obj = ContentFile(temp_thumb.read())
      data_obj.name = self.file.name

      self.thumbnail = data_obj

      temp_thumb.close()
    except:
      return

  def save(self, *args, **kwargs):
    self.create_thumbnail()
    super(Option_file, self).save(*args, **kwargs)

@receiver(pre_delete, sender=Option_file)
def option_file_model_delete(sender, instance, **kwargs):
  if instance.file.name:
    instance.file.delete(False)

class Job(models.Model):
  specialist = models.ForeignKey(
    Specialist, null=True, default=None, blank=True,
    on_delete=models.SET_NULL, verbose_name='Специалист'
  )
  activity = models.ForeignKey(
    Activity, null=False,
    on_delete=models.CASCADE, verbose_name='Вид деятельности'
  )
  schedule = models.ForeignKey(
    Schedule, null=True, default=None, blank=True,
    on_delete=models.SET_NULL, verbose_name='Шаблон занятия'
  )
  methods = models.ManyToManyField(Method, verbose_name='Формы')

  reports = models.ManyToManyField('Exercise', through='Exercise_report', verbose_name='Отчеты по упражнениям')

  date = models.DateField(verbose_name='Дата проведения')
  start_time = models.TimeField(verbose_name='Время начала')

  topic = models.TextField(blank=True, verbose_name='Тема занятия')
  comment = models.TextField(blank=True, verbose_name='Комментарий по занятию')

  report_comment = models.TextField(blank=True, verbose_name='Комментарий по результатам занятия')

  def clear_params(self):
    self.topic = ''
    self.reports.clear()
    self.methods.clear()
    self.comment = ''
    self.job_file_set.all().delete()

  class Meta:
    db_table = 'job'
    verbose_name = 'Занятие'
    verbose_name_plural = 'Занятия'
    ordering = ['-date', '-start_time']

  def __str__(self):
    return '{0} с {1}'.format(
      self.date.strftime('%m.%d'),
      self.start_time.strftime('%H.%M')
    )

class Job_file(models.Model):
  def get_file_upload_to(instance, filename):
    return 'job_files/{0}/{1}/{2}/{3}'.format(
      instance.job.date.year,
      instance.job.date.month,
      instance.job.date.day,
      filename
    )
  def get_thumbnail_upload_to(instance, filename):
    return 'job_files/{0}/{1}/{2}/thumbnail_{3}'.format(
      instance.job.date.year,
      instance.job.date.month,
      instance.job.date.day,
      filename
    )

  job = models.ForeignKey(
    Job, null=False,
    on_delete=models.CASCADE, verbose_name='Занятие'
  )

  file = models.FileField(
    upload_to=get_file_upload_to,
    max_length=255,
    verbose_name='Файл'
  )

  thumbnail = models.ImageField(
    null=True,
    default=None,
    upload_to=get_thumbnail_upload_to,
    max_length=255,
    verbose_name='Миниатюра'
  )

  def create_thumbnail(self):
    try:
      file_name, file_extension = os.path.splitext(self.file.name)

      if file_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
      elif file_extension == '.gif':
        FTYPE = 'GIF'
      elif file_extension == '.png':
        FTYPE = 'PNG'
      else:
        return

      image = Image.open(self.file)
      image.thumbnail((200,200), Image.ANTIALIAS)

      temp_thumb = BytesIO()
      image.save(temp_thumb, FTYPE)
      temp_thumb.seek(0)

      data_obj = ContentFile(temp_thumb.read())
      data_obj.name = self.file.name

      self.thumbnail = data_obj

      temp_thumb.close()
    except:
      return

  def __str__(self):
    return self.file.name

  def save(self, *args, **kwargs):
    self.create_thumbnail()
    super(Job_file, self).save(*args, **kwargs)

  class Meta:
    db_table = 'job_file'
    verbose_name = 'Файл занятия'
    verbose_name_plural = 'Файлы занятия'
    ordering = ['job']

@receiver(pre_delete, sender=Job_file)
def job_file_model_delete(sender, instance, **kwargs):
  if instance.file.name:
    instance.file.delete(False)


class Job_report_file(models.Model):
  def get_file_upload_to(instance, filename):
    return 'job_report_files/{0}/{1}/{2}/{3}'.format(
      instance.job.date.year,
      instance.job.date.month,
      instance.job.date.day,
      filename
    )
  def get_thumbnail_upload_to(instance, filename):
    return 'job_report_files/{0}/{1}/{2}/thumbnail_{3}'.format(
      instance.job.date.year,
      instance.job.date.month,
      instance.job.date.day,
      filename
    )

  job = models.ForeignKey(
    Job, null=False,
    on_delete=models.CASCADE, verbose_name='Занятие'
  )

  file = models.FileField(
    upload_to=get_file_upload_to,
    max_length=255,
    verbose_name='Файл'
  )

  thumbnail = models.ImageField(
    null=True,
    default=None,
    upload_to=get_thumbnail_upload_to,
    max_length=255,
    verbose_name='Миниатюра'
  )

  def create_thumbnail(self):
    try:
      file_name, file_extension = os.path.splitext(self.file.name)

      if file_extension in ['.jpg', '.jpeg']:
        FTYPE = 'JPEG'
      elif file_extension == '.gif':
        FTYPE = 'GIF'
      elif file_extension == '.png':
        FTYPE = 'PNG'
      else:
        return

      image = Image.open(self.file)
      image.thumbnail((200,200), Image.ANTIALIAS)

      temp_thumb = BytesIO()
      image.save(temp_thumb, FTYPE)
      temp_thumb.seek(0)

      data_obj = ContentFile(temp_thumb.read())
      data_obj.name = self.file.name

      self.thumbnail = data_obj

      temp_thumb.close()
    except:
      return

  def __str__(self):
    return self.file.name

  def save(self, *args, **kwargs):
    self.create_thumbnail()
    super(Job_file, self).save(*args, **kwargs)

  class Meta:
    db_table = 'job_report_file'
    verbose_name = 'Файл отчета по занятию'
    verbose_name_plural = 'Файлы отчета по занятию'
    ordering = ['job']

@receiver(pre_delete, sender=Job_report_file)
def job_report_file_model_delete(sender, instance, **kwargs):
  if instance.file.name:
    instance.file.delete(False)


class Exercise_report(models.Model):
  MARK_CHOICES = (
    (0, 'Неудовлетворительно'),
    (1, 'Удовлетворительно'),
    (2, 'Хорошо'),
  )

  job = models.ForeignKey(
    Job, null=False,
    on_delete=models.CASCADE, verbose_name='Занятие'
  )
  exercise = models.ForeignKey(
    Exercise, null=False,
    on_delete=models.CASCADE, verbose_name='Упражнение'
  )

  mark = models.PositiveSmallIntegerField(
    null=True, blank=True, default=None,
    choices=MARK_CHOICES,
    verbose_name='Успешность оттачивания навыка')

  class Meta:
    db_table = 'exercise_report'
    verbose_name = 'Отчет по упражнению'
    verbose_name_plural = 'Отчеты по упражнению'
    ordering = ['job', 'exercise']
    unique_together = ('job', 'exercise')

  def __str__(self):
    return 'Оценка за {0}: {1}'.format(
      self.job,
      'Не выставлена' if self.mark is None else self.get_mark_display()
    )

class Mission(models.Model):
  '''
    Задача
  '''
  STATUS_CHOICES = (
    (0, 'Новое'),
    (1, 'В процессе'),
    (2, 'Исполнено'),
  )

  director = models.ForeignKey(
    Specialist, null=False, related_name='director_missions',
    on_delete=models.CASCADE, verbose_name='Постановщик'
  )
  executor = models.ForeignKey(
    Specialist, null=False, related_name='executor_missions',
    on_delete=models.CASCADE, verbose_name='Исполнитель'
  )
  controller = models.ForeignKey(
    Specialist, null=True, related_name='controller_missions',
    blank=True,
    on_delete=models.CASCADE, verbose_name='Контролер'
  )

  creation_date = models.DateTimeField(
    auto_now_add=True,
    null=False, verbose_name='Дата-время создания'
  )
  deadline = models.DateField(null=True, blank=True, verbose_name='Срок исполнения')
  caption = models.TextField(blank=False, verbose_name='Название')
  comment = models.TextField(blank=True, verbose_name='Комментарий')
  status = models.PositiveSmallIntegerField(
    default=0, null=False, choices=STATUS_CHOICES,
    blank=False, verbose_name='Статус поручения'
  )

  class Meta:
    db_table = 'mission'
    verbose_name = 'Задача'
    verbose_name_plural = 'Задачи'
    ordering = ['-creation_date',]

  def __str__(self):
    return self.caption


class Announcement(models.Model):
  '''
    Обращения руководства
  '''

  creation_date = models.DateTimeField(
    auto_now_add=True,
    null=False, verbose_name='Дата-время создания'
  )
  caption = models.TextField(blank=False, verbose_name='Краткое описание')
  text = models.TextField(blank=False, verbose_name='Текст обращения')

  class Meta:
    db_table = 'announcement'
    verbose_name = 'Обращение руководства'
    verbose_name_plural = 'Обращения руководства'
    ordering = ['-creation_date',]

  def __str__(self):
    return self.caption

class Appeal(models.Model):
  '''
    Тема обращения к руководству
  '''

  creator = models.ForeignKey(
    Specialist, null=False,
    on_delete=models.CASCADE, verbose_name='Обратившийся'
  )

  creation_date = models.DateTimeField(
    auto_now_add=True,
    null=False, verbose_name='Дата-время создания'
  )
  theme = models.TextField(blank=False, verbose_name='Тема обращения')
  closed = models.BooleanField(
    default=False, verbose_name='Закрыто'
  )

  class Meta:
    db_table = 'appeal'
    verbose_name = 'Обращение к руководсву'
    verbose_name_plural = 'Обращения к руководсву'
    ordering = ['-creation_date',]

  def __str__(self):
    return self.theme

class Message(models.Model):
  '''
    Сообщение в теме обращения к руководству
  '''
  appeal = models.ForeignKey(
    Appeal, null=False,
    on_delete=models.CASCADE, verbose_name='Обращение'
  )
  author = models.ForeignKey(
    Specialist, null=False,
    on_delete=models.CASCADE, verbose_name='Автор'
  )

  text = models.TextField(blank=True, verbose_name='Текст')
  file = models.FileField(
    null=True, blank=True,
    upload_to='message_files/%Y/%m/%d/',
    max_length=255,
    verbose_name='Прикрепленный файл'
  )
  reply = models.BooleanField(
    default=False, verbose_name='Ответ руководства'
  )
  creation_date = models.DateTimeField(
    auto_now_add=True,
    null=False, verbose_name='Дата-время написания'
  )

  def filename(self):
    if (self.file):
      return os.path.basename(self.file.name)
    else:
      return None

  class Meta:
    db_table = 'message'
    verbose_name = 'Сообщение обращения'
    verbose_name_plural = 'Сообщения обращения'
    ordering = ['creation_date',]

  def __str__(self):
    return self.text

@receiver(post_save, sender=Message)
def messages_create_notifications(sender, instance, **kwargs):
  try:
    if (instance.author.user.is_staff == False):
      admins = User.objects.filter(is_staff = True).values_list('id', flat=True)
      for admin in admins:
        Notification.objects.create(user_id=admin, type=1, meta=json.dumps({'appeal_id': instance.appeal_id}))
      loop.run_until_complete(send_message({'action': 'notifications.update.1', 'appeal_id': instance.appeal_id,
                                            'type': 'list',
                                            'list_idx': list(admins)}, settings.WS_IP))
    elif (instance.author.user.is_staff == True and instance.appeal.creator_id == instance.author_id):
      admins = User.objects.filter(is_staff=True).exclude(id=instance.author.user_id).values_list('id', flat=True)
      for admin in admins:
        Notification.objects.create(user_id=admin, type=1, meta=json.dumps({'appeal_id': instance.appeal_id}))
      loop.run_until_complete(send_message({'action': 'notifications.update.1', 'appeal_id': instance.appeal_id,
                                            'type': 'list',
                                            'list_idx': list(admins)}, settings.WS_IP))
    elif (instance.author.user.is_staff == True and instance.appeal.creator_id != instance.author_id):
      Notification.objects.create(user_id=instance.appeal.creator.user_id,
                                  type=1, meta=json.dumps({'appeal_id': instance.appeal_id}))
      loop.run_until_complete(send_message({'action': 'notifications.update.1', 'appeal_id': instance.appeal_id,
                                            'type': 'to',
                                            'to_id': instance.appeal.creator.user_id}, settings.WS_IP))
  except:
    pass

class Task_group(models.Model):
  '''
    Интервенционная группа
  '''
  author = models.ForeignKey(
    Specialist, null=True,
    on_delete=models.CASCADE, verbose_name='Автор записи',
    related_name='author_task_groups'
  )
  responsible = models.ForeignKey(
    Specialist,
    null=True, blank=True,
    on_delete=models.CASCADE, verbose_name='Ответственный',
    related_name='responsible_task_groups'
  )

  text = models.TextField(blank=False, verbose_name='Текст')
  solution = models.TextField(blank=True, verbose_name='Решение')
  deadline = models.DateField(blank=True, null=True, verbose_name='Срок')
  is_question = models.BooleanField(default=False, verbose_name='Является ли вопросом')
  creation_date = models.DateTimeField(
    auto_now_add=True,
    null=False, verbose_name='Дата-время написания'
  )

  class Meta:
    db_table = 'task_group'
    verbose_name = 'Интервенционная группа'
    verbose_name_plural = 'Интервенционные группы'
    ordering = ['-creation_date',]

  def __str__(self):
    return self.text

class Talent(models.Model):
  '''
    Талант
  '''
  specialist = models.ForeignKey(
    Specialist, null=False,
    on_delete=models.CASCADE, verbose_name='Специалист'
  )
  area = models.ForeignKey(
    Educational_area, null=False,
    on_delete=models.CASCADE, verbose_name='Образовательная область'
  )

  name = models.TextField(blank=False, verbose_name='Название')
  text = models.TextField(blank=True, verbose_name='Описание')
  creation_date = models.DateTimeField(
    auto_now_add=True,
    null=False, verbose_name='Дата-время написания'
  )

  class Meta:
    db_table = 'talent'
    verbose_name = 'Талант'
    verbose_name_plural = 'Таланты'
    ordering = ['-creation_date',]

  def __str__(self):
    return self.text

class Notification(models.Model):
  '''
    Уведомление
  '''
  type_choices = [
    (0, 'Задачи'),
    (1, 'Обращения к руководству'),
    (2, 'Важная информация'),
  ]

  type = models.PositiveSmallIntegerField(
    choices=type_choices, null=False, verbose_name='Тип уведомления'
  )
  user = models.ForeignKey(
    User, null=False,
    on_delete=models.CASCADE, verbose_name='Пользователь'
  )
  meta = JSONField(verbose_name='Meta', blank=True, null=True)

  class Meta:
    db_table = 'notification'
    verbose_name = 'Уведомление'
    verbose_name_plural = 'Уведомления'
