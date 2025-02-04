from django.db.models import Func

class UpdateRightBound(Func):
  """
  Первый параметр - имя поля DateRange
  Второй параметр именованный right_bound - строка с датой
  """
  function = 'daterange'
  template = '%(function)s(LOWER(%(expressions)s), \'%(right_bound)s\')'