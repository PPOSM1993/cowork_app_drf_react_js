from rest_framework import serializers
from .models import Referral

class ReferralSerializer(serializers.ModelSerializer):
    referrer_email = serializers.EmailField(source='referrer.email', read_only=True)
    referral_code = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Referral
        fields = '__all__'

    def validate_referred_email(self, value):
        if not value:
            raise serializers.ValidationError("Debes proporcionar un correo electrónico válido.")
        if Referral.objects.filter(referred_email=value, status='pending').exists():
            raise serializers.ValidationError("Ya existe una invitación pendiente para este correo.")
        return value

    def validate(self, attrs):
        referrer = attrs.get('referrer')
        referred_email = attrs.get('referred_email')

        if referrer and referrer.email == referred_email:
            raise serializers.ValidationError("No puedes referirte a ti mismo.")

        return attrs
