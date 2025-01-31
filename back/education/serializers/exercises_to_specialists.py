from rest_framework import serializers

from education.models import Exercise, Specialist

class RemoveExerciseSerializer(serializers.Serializer):
  exercise = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all(), label='Упражнение')
  specialists = serializers.PrimaryKeyRelatedField(queryset=Specialist.objects.all(), many=True, label='Специалисты')

