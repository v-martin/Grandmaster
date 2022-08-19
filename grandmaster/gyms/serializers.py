from rest_framework import serializers
from .models import Gym


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = [
            'id',
            'title',
            'description',
            'address',
            'cover',
            'order',
            'trainers',
        ]
        read_only_fields = ['id']