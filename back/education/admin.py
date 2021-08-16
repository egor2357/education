from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import *

class SessionAdmin(admin.ModelAdmin):
  def _session_data(self, obj):
    return obj.get_decoded()
  list_display = ['session_key', '_session_data', 'expire_date']
admin.site.register(Session, SessionAdmin)

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
  list_display = ('__str__', 'user', 'is_active')
  list_filter = ('is_active',)
  inlines = (CompetenceInline, SpecialtyInline)

admin.site.register(Specialist, SpecialistAdmin)

class PresenceAdmin(admin.ModelAdmin):
  list_filter = ('specialist', 'is_available')
  list_display = (
    'specialist', 'main_interval',
    'date_from', 'date_to',
    'is_available'
  )

admin.site.register(Presence, PresenceAdmin)

class ScheduleInline(admin.TabularInline):
  model = Schedule
  extra = 0

class ScheduleAdmin(admin.ModelAdmin):
  search_fields = ('activity_name',)
  list_filter = ('day',)

admin.site.register(Schedule, ScheduleAdmin)

class ActivityAdmin(admin.ModelAdmin):
  search_fields = ('name',)
  list_display = ('name', 'color')
  filter_horizontal = ('skills',)
  inlines = (ScheduleInline,)

admin.site.register(Activity, ActivityAdmin)

class Option_fileInline(admin.TabularInline):
  model = Option_file
  extra = 0

class Option_fileAdmin(admin.ModelAdmin):
  list_filter = ('option',)

admin.site.register(Option_file, Option_fileAdmin)

class OptionAdmin(admin.ModelAdmin):
  search_fields = ('topic', 'comment')
  list_display = ('specialist', 'activity', 'topic')
  list_filter = ('specialist', 'activity')
  filter_horizontal = ('skills',)
  inlines = (Option_fileInline,)

admin.site.register(Option, OptionAdmin)

class Job_fileInline(admin.TabularInline):
  model = Job_file
  extra = 0

class Job_fileAdmin(admin.ModelAdmin):
  list_filter = ('job',)

admin.site.register(Job_file, Job_fileAdmin)

class Skill_reportInline(admin.TabularInline):
  model = Skill_report
  extra = 0

class Skill_reportAdmin(admin.ModelAdmin):
  list_filter = ('job', 'skill')
  list_display = ('job', 'skill', 'mark', 'coefficient',)

admin.site.register(Skill_report, Skill_reportAdmin)

class JobAdmin(admin.ModelAdmin):
  search_fields = ('topic', 'comment')
  list_display = (
    'activity', 'date',
    'specialist', 'schedule',
    'start_time', 'topic')
  list_filter = ('schedule',)
  inlines = (Job_fileInline, Skill_reportInline)
  date_hierarchy = 'date'

admin.site.register(Job, JobAdmin)

class MissionAdmin(admin.ModelAdmin):
  list_filter = ('director', 'executor', 'controller', 'status')
  list_display = ('caption', 'deadline', 'director', 'executor', 'controller', 'status')
  search_fields = ('caption', 'comment')

admin.site.register(Mission, MissionAdmin)

class AnnouncementAdmin(admin.ModelAdmin):
  list_display = ('creation_date', 'caption', 'text',)
  search_fields = ('caption', 'text')

admin.site.register(Announcement, AnnouncementAdmin)

class AppealAdmin(admin.ModelAdmin):
  list_filter = ('creation_date', 'closed',)
  list_display = ('creator', 'creation_date', 'theme', 'closed',)
  search_fields = ('theme',)

admin.site.register(Appeal, AppealAdmin)

class MessageAdmin(admin.ModelAdmin):
  list_filter = ('creation_date', 'reply', 'appeal')
  list_display = ('appeal', 'author', 'reply', 'creation_date', 'text',)
  search_fields = ('text',)

admin.site.register(Message, MessageAdmin)