from django.contrib import admin

from .models import Educational_area, Development_direction, Skill, Form, Method

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