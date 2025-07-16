from rest_framework import serializers
from .models import SupportTicket


class SupportTicketSerializer(serializers.ModelSerializer):
    created_by_email = serializers.EmailField(source='created_by.email', read_only=True)
    assigned_to_email = serializers.EmailField(source='assigned_to.email', read_only=True)

    class Meta:
        model = SupportTicket
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'created_by',
            'created_by_email',
            'assigned_to',
            'assigned_to_email',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_by_email', 'created_at', 'updated_at']

    def validate_priority(self, value):
        valid_priorities = [choice[0] for choice in SupportTicket.PRIORITY_CHOICES]
        if value not in valid_priorities:
            raise serializers.ValidationError("Prioridad inválida.")
        return value

    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in SupportTicket.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError("Estado inválido.")
        return value

    def validate_assigned_to(self, value):
        if value and not value.is_staff:
            raise serializers.ValidationError("Solo personal autorizado puede ser asignado al ticket.")
        return value

    def validate(self, data):
        if self.instance and self.instance.status == 'closed':
            if data.get('status') and data.get('status') != 'closed':
                raise serializers.ValidationError("No puedes reabrir un ticket cerrado.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)
