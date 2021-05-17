from django.contrib import admin

from .models import Educational_area, Development_direction, Skill, Form, Method
from .models import Specialist, Competence, Specialty, Presense
from .models import Activity, Schedule

# Register your models here.
class Educational_areaAdmin(admin.ModelAdmin):
  search_fields = ('name', 'number')
  list_display = ('number', 'name')

admin.site.register(Educational_area, Educational_areaAdmin)

class Development_directionAdmin(admin.ModelAdmin):
  search_fields = ('name', 'number')
  list_display = ('number', 'name', 'area')
  list_filter = ('area',)

admin.site.register(Development_direction, Development_directionAdmin)

class SkillAdmin(admin.ModelAdmin):
  search_fields = ('name', 'number')
  list_display = ('number', 'name', 'direction')
  list_filter = ('direction',)

admin.site.register(Skill, SkillAdmin)

class FormAdmin(admin.ModelAdmin):
  search_fields = ('name',)
  list_display = ('name',)

admin.site.register(Form, FormAdmin)

class MethodAdmin(admin.ModelAdmin):
  search_fields = ('name',)
  list_display = ('name', 'form')
  list_filter = ('form',)

admin.site.register(Method, MethodAdmin)

class CompetenceInline(admin.TabularInline):
  model = Competence
  extra = 0

class CompetenceAdmin(admin.ModelAdmin):
  list_display = ('specialist', 'skill', 'coefficient')
  list_filter = ('specialist', 'skill')

admin.site.register(Competence, CompetenceAdmin)

class SpecialtyInline(admin.TabularInline):
  model = Specialty
  extra = 0

class SpecialtyAdmin(admin.ModelAdmin):
  list_display = ('specialist', 'activity', 'is_main')
  list_filter = ('specialist', 'activity')

admin.site.register(Specialty, SpecialtyAdmin)

class SpecialistAdmin(admin.ModelAdmin):
  search_fields = ('surname', 'name', 'patronymic', 'role')
  list_display = ('__str__', 'user')
  inlines = (CompetenceInline, SpecialtyInline)

admin.site.register(Specialist, SpecialistAdmin)

class PresenseAdmin(admin.ModelAdmin):
  list_filter = ('specialist', 'is_available')
  list_display = ('specialist', 'date_from', 'date_to', 'is_available')

admin.site.register(Presense, PresenseAdmin)

class ScheduleInline(admin.TabularInline):
  model = Schedule
  extra = 0

class ScheduleAdmin(admin.ModelAdmin):
  search_fields = ('activity_name',)
  list_filter = ('day', )

admin.site.register(Schedule, ScheduleAdmin)

class ActivityAdmin(admin.ModelAdmin):
  search_fields = ('name',)
  list_display = ('name', 'color')
  filter_horizontal = ('skills',)
  inlines = (ScheduleInline,)

admin.site.register(Activity, ActivityAdmin)