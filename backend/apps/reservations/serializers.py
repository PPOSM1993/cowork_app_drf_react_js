from rest_framework import serializers
from .models import Reservation
from django.utils import timezone

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate_start_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("La fecha/hora de inicio no puede estar en el pasado.")
        return value

    def validate_end_datetime(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("La fecha/hora de término no puede estar en el pasado.")
        return value

    def validate(self, data):
        start = data.get('start_datetime')
        end = data.get('end_datetime')

        if start and end and start >= end:
            raise serializers.ValidationError("La fecha/hora de inicio debe ser anterior a la de fin.")

        # Validación de solapamiento de reservas (opcional pero profesional)
        overlapping = Reservation.objects.filter(
            space=data.get('space'),
            start_datetime__lt=end,
            end_datetime__gt=start
        )
        if self.instance:
            overlapping = overlapping.exclude(pk=self.instance.pk)

        if overlapping.exists():
            raise serializers.ValidationError("El espacio ya está reservado en ese rango de tiempo.")

        return data
