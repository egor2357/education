from rest_framework import serializers

from education.models import (
  Exercise_to_specialist,
  Exercise, Specialist, Result, Skill, Development_direction, Educational_area
)

class Exercise_to_specialistSerializer(serializers.ModelSerializer):
  exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all(), label='Упражнение')
  specialist = serializers.PrimaryKeyRelatedField(queryset=Specialist.objects.all(), label='Специалист')

  class Meta:
    model = Exercise_to_specialist
    fields = '__all__'

class Exercise_to_specialistsSerializer(serializers.Serializer):
  exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all(), label='Упражнение')
  specialists = serializers.PrimaryKeyRelatedField(queryset=Specialist.objects.all(), many=True, label='Специалисты')

class Result_to_specialistsSerializer(serializers.Serializer):
  result = serializers.PrimaryKeyRelatedField(queryset=Result.objects.all(), label='Ожидаемый результат')
  specialists = serializers.PrimaryKeyRelatedField(queryset=Specialist.objects.all(), many=True, label='Специалисты')

class Skill_to_specialistsSerializer(serializers.Serializer):
  skill = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), label='Навык')
  specialists = serializers.PrimaryKeyRelatedField(queryset=Specialist.objects.all(), many=True, label='Специалисты')

class Development_direction_to_specialistsSerializer(serializers.Serializer):
  direction = serializers.PrimaryKeyRelatedField(queryset=Development_direction.objects.all(), label='Направление развития')
  specialists = serializers.PrimaryKeyRelatedField(queryset=Specialist.objects.all(), many=True, label='Специалисты')

class Educational_area_to_specialistsSerializer(serializers.Serializer):
  area = serializers.PrimaryKeyRelatedField(queryset=Educational_area.objects.all(), label='Образовательная область')
  specialists = serializers.PrimaryKeyRelatedField(queryset=Specialist.objects.all(), many=True, label='Специалисты')