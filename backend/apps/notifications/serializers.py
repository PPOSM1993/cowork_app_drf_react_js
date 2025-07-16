from rest_framework import serializers
from .models import Notification
from django.utils import timezone


class NotificationSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    read_status_display = serializers.CharField(source='get_read_status_display', read_only=True)

    class Meta:
        model = Notification
        fields = '__all__'

    def validate_message(self, value):
        """
        Ensure that the message isn't empty or too short.
        """
        if len(value.strip()) == 0:
            raise serializers.ValidationError("El mensaje no puede estar vacío.")
        return value

    def get_age(self, obj):
        """
        Returns the time difference from now until the notification was created.
        """
        time_difference = timezone.now() - obj.created_at
        return str(time_difference).split('.')[0]  # Return as human-readable string (hours, minutes)
