from django.db import models
from django.contrib.auth.models import User

class Educational_area(models.Model):
  name = models.TextField(max_length=200, verbose_name='Название')
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
    on_delete=models.CASCADE, verbose_name=u'Образовательная область'
  )

  name = models.TextField(max_length=200, verbose_name='Название')
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
    on_delete=models.CASCADE, verbose_name=u'Направление развития'
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
    on_delete=models.SET_NULL, verbose_name=u'Пользователь'
  )

  surname = models.TextField(max_length=200, verbose_name='Фамилия')
  name = models.TextField(max_length=200, verbose_name='Имя')
  patronymic = models.TextField(max_length=200, verbose_name='Отчество')
  role = models.TextField(max_length=200, verbose_name='Роль')


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
        res += '{0}.{1}.'.format(self.name[0], self.patronymic[0])
    elif self.user:
      res = self.user.login
    else:
      res = '{0} {1} {2}'.format(self.surname, self.name, self.patronymic)

    return res

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
    on_delete=models.CASCADE, verbose_name=u'Форма'
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
  name = models.TextField(max_length=200, verbose_name='Название')
  color = models.CharField(max_length=7, default='#CCCCCC', blank=True, verbose_name=u'Код цвета')

  class Meta:
    db_table = 'activity'
    verbose_name = 'Вид деятельности'
    verbose_name_plural = 'Виды деятельности'
    ordering = ['name']

  def __str__(self):
    return self.name

class Schedule(models.Model):
  activity = models.ForeignKey(
    Activity, null=False,
    on_delete=models.CASCADE, verbose_name=u'Вид деятельности'
  )

  day = models.PositiveSmallIntegerField(verbose_name='Индекс дня недели')
  start_time = models.TimeField(verbose_name='Время начала')

  weekday_names = [
    'Понедельник', 'Вторник',
    'Среда', 'Четверг',
    'Пятница', 'Суббота', 'Воскресенье'
  ]

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