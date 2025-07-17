from rest_framework import serializers
from .models import IdentityVerification
from django.utils import timezone

class IdentityVerificationSerializer(serializers.ModelSerializer):
    document_front_image = serializers.ImageField(required=True)
    document_back_image = serializers.ImageField(required=False, allow_null=True)
    selfie_image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = IdentityVerification
        fields = [
            'id',
            'user',
            'document_type',
            'document_number',
            'document_front_image',
            'document_back_image',
            'selfie_image',
            'status',
            'submitted_at',
            'reviewed_at',
            'review_comments',
        ]
        read_only_fields = ['status', 'submitted_at', 'reviewed_at', 'review_comments']

    def validate_document_number(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError('El número del documento es demasiado corto.')
        return value.strip()

    def validate(self, data):
        document_type = data.get('document_type')
        front_image = data.get('document_front_image')
        selfie = data.get('selfie_image')

        if document_type in ['dni', 'passport', 'license'] and not front_image:
            raise serializers.ValidationError('Debe adjuntar la imagen frontal del documento.')

        if document_type != 'other' and not selfie:
            raise serializers.ValidationError('Debe subir una selfie para este tipo de documento.')

        return data

    def create(self, validated_data):
        validated_data['submitted_at'] = timezone.now()
        return super().create(validated_data)
