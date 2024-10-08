from rest_framework import serializers

from .models import Feature

class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'

        model = Feature
   