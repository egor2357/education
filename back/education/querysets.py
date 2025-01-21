from .models import *

def getEducational_areaQueryset(request):
    return Educational_area.objects.all().prefetch_related(
        'development_direction_set',
        'development_direction_set__skill_set',
        'development_direction_set__skill_set__result_set',
        'development_direction_set__skill_set__result_set__exercises',
      )