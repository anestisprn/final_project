from rest_framework import serializers
from .models import *


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourExperience
        fields = '__all__'