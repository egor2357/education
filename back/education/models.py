from django.db import models

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