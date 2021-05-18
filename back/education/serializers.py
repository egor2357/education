from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import *

#create your serializers here.
class LoginSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField()

  def validate(self, data):
    username = data.get('username', None)
    password = data.get('password', None)

    if username is None:
      raise serializers.ValidationError(
        'Логин пользователя не введен'
      )
    if password is None:
      raise serializers.ValidationError(
        'Пароль пользователя не введен'
      )

    user = authenticate(username=username, password=password)

    if user is None:
      raise serializers.ValidationError(
        'Логин или пароль пользователя не верен'
      )
    if not user.is_active:
      raise serializers.ValidationError(
        'Пользователь не активен'
      )

    return {'user': user}

class SpecialistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Specialist
    fields = ['surname', 'name', 'patronymic', 'role']


class UserSerializer(serializers.ModelSerializer):
  specialist = SpecialistSerializer(read_only=True)
  class Meta:
    model = User
    fields = ['id', 'username', 'is_staff', 'password', 'specialist']

  def create(self, validated_data):
    user = super().create(validated_data)
    user.set_password(validated_data['password'])
    user.save()
    return user

  def update(self, instance, validated_data):
    instance.username = validated_data['username']
    instance.set_password(validated_data['password'])
    instance.save()
    return instance

class SkillSerializer(serializers.ModelSerializer):
  direction_id = serializers.IntegerField()
  class Meta:
    model = Skill
    fields = ('id', 'name', 'number', 'direction_id')

class Development_directionSerializer(serializers.ModelSerializer):
  area_id = serializers.IntegerField()
  skills = SkillSerializer(
    source='skill_set', many=True, read_only=True
  )
  class Meta:
    model = Development_direction
    fields = ('id', 'name', 'number', 'skills', 'area_id')

class Educational_areaSerializer(serializers.ModelSerializer):
  development_directions = Development_directionSerializer(
    source='development_direction_set', many=True, read_only=True
  )
  class Meta:
    model = Educational_area
    fields = ('id', 'name', 'number', 'development_directions')
