import json
from .models import *

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

  if 'skills' in request.data:
    skills = json.loads(request.data['skills'])
    skills = Skill.objects.filter(pk__in=skills)
    option.skills.clear()
    option.skills.set(skills)

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

  if 'reports' in request.data:
    skills = json.loads(request.data['reports'])

    curr_skill_reports_ids = list(job.skill_report_set.all().values_list('skill_id', flat=True))

    skills_to_save = []
    remaining_skills = []

    for skill_id in skills:
      if skill_id not in curr_skill_reports_ids:
        skills_to_save.append(
          Skill_report(job=job, skill_id=skill_id)
        )
      else:
        remaining_skills.append(skill_id)

    skill_reports_qs = job.skill_report_set.all()
    skill_reports_qs.exclude(skill_id__in=remaining_skills).delete()
    Skill_report.objects.bulk_create(skills_to_save)

  if 'methods' in request.data:
    methods = json.loads(request.data['methods'])
    methods = Method.objects.filter(pk__in=methods)
    job.methods.set(methods)

  if 'marks' in request.data:
    user = request.user
    coeff_by_skill_id = dict(list(user.specialist.competence_set.all().values_list('skill_id', 'coefficient')))

    marks = request.data.get('marks', [])
    for mark in marks:
      skill_report = Skill_report.objects.get(pk=mark['id'])
      skill_report.coefficient = coeff_by_skill_id[skill_report.skill_id]
      skill_report.mark = mark['mark']
      skill_report.save()

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