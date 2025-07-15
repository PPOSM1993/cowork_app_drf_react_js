from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    REPORT_TYPE_CHOICES = ['Ventas', 'Reservas', 'Usuarios', 'Finanzas']

    report_type = serializers.ChoiceField(choices=REPORT_TYPE_CHOICES)
    report_file_url = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('generated_at', 'last_modified', 'created_by')

    def get_report_file_url(self, obj):
        if hasattr(obj, 'file') and obj.file:
            return obj.file.url
        return None

    def validate_title(self, value):
        value = value.strip().title()
        if len(value) < 5:
            raise serializers.ValidationError("El título debe tener al menos 5 caracteres.")
        return value

    def validate_description(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError("La descripción es obligatoria y debe ser más descriptiva.")
        return value

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        data.pop('created_by', None)
        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)
