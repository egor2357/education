from django.db import models
from django.contrib.auth.models import User

class Educational_area(models.Model):
  name = models.TextField(max_length=200, unique=True, verbose_name='Название')
  number = models.PositiveSmallIntegerField(verbose_name='Номер')

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

  name = models.TextField(max_length=200, unique=True, verbose_name='Название')
  number = models.PositiveSmallIntegerField(verbose_name='Номер')

  class Meta:
    db_table = 'development_direction'
    verbose_name = 'Направление развития'
    verbose_name_plural = 'Направления развития'
    ordering = ['number']

  def __str__(self):
    return self.name

class Skill(models.Model):
  direction = models.ForeignKey(
    Development_direction, null=False,
    on_delete=models.CASCADE, verbose_name='Направление развития'
  )

  name = models.TextField(max_length=200, verbose_name='Название')
  number = models.PositiveSmallIntegerField(verbose_name='Номер')

  class Meta:
    db_table = 'skill'
    verbose_name = 'Навык'
    verbose_name_plural = 'Навыки'
    ordering = ['number']

  def __str__(self):
    return self.name

class Specialist(models.Model):
  user = models.OneToOneField(
    User, null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Пользователь'
  )

  skills = models.ManyToManyField(Skill, through='Competence', verbose_name='Развиваемые навыки')
  activities = models.ManyToManyField('Activity', through='Specialty', verbose_name='Направления деятельности')

  surname = models.CharField(max_length=20, blank=True, verbose_name='Фамилия')
  name = models.CharField(max_length=20, blank=True, verbose_name='Имя')
  patronymic = models.CharField(max_length=20, blank=True, verbose_name='Отчество')
  role = models.TextField(max_length=200, blank=True, verbose_name='Роль')
  is_active = models.BooleanField(default=True, verbose_name='Активен ли')

  @classmethod
  def get_available(self, template, date):
    available_specs_ids = (template.activity.specialty_set.filter(is_main=True)
                                                            .values_list('specialist_id', flat=True))

    presense_specs_ids = Presence.objects.filter(
      specialist_id__in=available_specs_ids,
      date_from__lte=date,
      date_to__gte=date,
      is_available=True
    ).values_list('specialist_id', flat=True)

    specialists = Specialist.objects.filter(pk__in=presense_specs_ids)

    if specialists.exists():
      specialist = specialists.first()
    else:
      specialist = None

    return specialist

  class Meta:
    db_table = 'specialist'
    verbose_name = 'Специалист'
    verbose_name_plural = 'Специалисты'
    ordering = ['surname']

  def __str__(self):
    res = ''
    if (self.surname):
      res += self.surname
      if (self.name and self.patronymic):
        res += ' {0}. {1}.'.format(self.name[0], self.patronymic[0])
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
  name = models.TextField(max_length=200, verbose_name='Название')

  class Meta:
    db_table = 'form'
    verbose_name = 'Форма проведения занятий'
    verbose_name_plural = 'Формы проведения занятий'
    ordering = ['name']

  def __str__(self):
    return self.name

class Method(models.Model):
  form = models.ForeignKey(
    Form, null=False,
    on_delete=models.CASCADE, verbose_name='Форма'
  )

  name = models.TextField(max_length=200, verbose_name='Название')

  class Meta:
    db_table = 'method'
    verbose_name = 'Способ проведения занятия'
    verbose_name_plural = 'Способы проведения занятия'
    ordering = ['name']

  def __str__(self):
    return self.name

class Activity(models.Model):
  skills = models.ManyToManyField(Skill, verbose_name='Развиваемые навыки')

  name = models.TextField(max_length=200, verbose_name='Название')
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

class Competence(models.Model):
  specialist = models.ForeignKey(
    Specialist,
    on_delete=models.CASCADE, verbose_name='Специалист'
  )
  skill = models.ForeignKey(
    Skill,
    on_delete=models.CASCADE, verbose_name='Навык'
  )

  coefficient = models.FloatField(verbose_name='Коэффициент')

  class Meta:
    db_table = 'competence'
    verbose_name = 'Компетенция специалиста'
    verbose_name_plural = 'Компетенции специалиста'
    unique_together = ('specialist', 'skill')
    ordering = ['specialist', 'skill']

  def __str__(self):
    return '{0} развивает {1}'.format(
      self.specialist,
      self.skill
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

class Option(models.Model):
  method = models.ForeignKey(
    Method, null=True, blank=True,
    on_delete=models.SET_NULL, verbose_name='Способ проведения занятия'
  )
  specialist = models.ForeignKey(
    Specialist, null=True,
    on_delete=models.SET_NULL, verbose_name='Специалист'
  )
  activity = models.ForeignKey(
    Activity, null=False,
    on_delete=models.CASCADE, verbose_name='Вид деятельсности')

  skills = models.ManyToManyField(Skill, verbose_name='Развиваемые на занятии навыки')

  caption = models.TextField(max_length=200, blank=True, verbose_name='Подпись')

  class Meta:
    db_table = 'option'
    verbose_name = 'Вариант занятия'
    verbose_name_plural = 'Варианты занятия'
    ordering = ['specialist']

  def __str__(self):
    return '{0} ({1}, {2})'.format(
      self.caption,
      self.specialist,
      self.activity
    )

class Option_file(models.Model):
  def get_file_upload_to(instance, filename):
    return 'option_files/{0}/{1}/{2}/{3}'.format(
      instance.option.activity.name,
      instance.option.specialist,
      instance.option.caption,
      filename
    )

  option = models.ForeignKey(
    Option, null=False,
    on_delete=models.CASCADE, verbose_name='Вариант занятия'
  )

  file = models.FileField(
    upload_to=get_file_upload_to,
    max_length=300,
    verbose_name='Файл'
  )

  class Meta:
    db_table = 'option_file'
    verbose_name = 'Файл варианта занятия'
    verbose_name_plural = 'Файлы варианта занятия'
    ordering = ['option']

  def __str__(self):
    return self.file.name

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

  reports = models.ManyToManyField('Skill', through='Skill_report', verbose_name='Отчеты по навыкам')

  date = models.DateField(verbose_name='Дата проведения')
  start_time = models.TimeField(verbose_name='Время начала')
  comment = models.TextField(blank=True, verbose_name='Комментарий по занятию')

  class Meta:
    db_table = 'job'
    verbose_name = 'Занятие'
    verbose_name_plural = 'Занятия'
    ordering = ['date']

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

  job = models.ForeignKey(
    Job, null=False,
    on_delete=models.CASCADE, verbose_name='Занятие'
  )

  file = models.FileField(
    upload_to=get_file_upload_to,
    max_length=200,
    verbose_name='Файл'
  )

  class Meta:
    db_table = 'job_file'
    verbose_name = 'Файл занятия'
    verbose_name_plural = 'Файлы занятия'
    ordering = ['job']

  def __str__(self):
    return self.file.name

class Skill_report(models.Model):
  marks = ['Неудовлетворительно', 'Удовлетворительно', 'Хорошо']
  mark_choices = [item for item in enumerate(marks)]

  job = models.ForeignKey(
    Job, null=False,
    on_delete=models.CASCADE, verbose_name='Занятие'
  )
  skill = models.ForeignKey(
    Skill, null=False,
    on_delete=models.CASCADE, verbose_name='Навык'
  )

  mark = models.PositiveSmallIntegerField(choices=mark_choices, verbose_name='Успешность оттачивания навыка')
  comment = models.TextField(blank=True, verbose_name='Комментарий по занятию')

  class Meta:
    db_table = 'skill_report'
    verbose_name = 'Отчет по навыку'
    verbose_name_plural = 'Отчеты по навыку'
    ordering = ['job']
    unique_together = ('job', 'skill')

  def __str__(self):
    return 'Оценка за {0}: {1}'.format(
      self.job,
      self.marks[self.mark]
    )