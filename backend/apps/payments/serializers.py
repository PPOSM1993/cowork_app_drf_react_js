from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            'id', 'customer', 'reservation',
            'amount', 'discount', 'tax', 'total_amount',
            'method', 'status', 'payment_date', 'notes'
        ]
        read_only_fields = ['id', 'payment_date', 'total_amount']

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("El monto debe ser mayor a 0.")
        return value

    def validate_discount(self, value):
        if value < 0:
            raise serializers.ValidationError("El descuento no puede ser negativo.")
        return value

    def validate_tax(self, value):
        if value < 0:
            raise serializers.ValidationError("El impuesto no puede ser negativo.")
        return value

    def validate(self, data):
        amount = data.get('amount', 0)
        discount = data.get('discount', 0)
        tax = data.get('tax', 0)

        total = (amount + tax) - discount
        if total < 0:
            raise serializers.ValidationError("El total a pagar no puede ser negativo.")

        if discount > amount:
            raise serializers.ValidationError("El descuento no puede superar el monto del pago.")

        return data
