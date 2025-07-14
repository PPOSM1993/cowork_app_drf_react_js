from rest_framework import serializers
from .models import Membership
from decimal import Decimal, ROUND_HALF_UP

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'usage_count')

    def validate_name(self, value):
        if Membership.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Ya existe una membresía con este nombre.")
        return value

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    def validate_usage_limit(self, value):
        if value is not None and value < 1:
            raise serializers.ValidationError("El límite de uso debe ser al menos 1 o dejarlo vacío para ilimitado.")
        return value

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        if start_date and end_date and end_date <= start_date:
            raise serializers.ValidationError("La fecha de fin debe ser posterior a la fecha de inicio.")

        return data
