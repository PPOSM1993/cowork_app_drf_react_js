from rest_framework import serializers
from .models import Invoice, InvoiceItem


class InvoiceItemSerializer(serializers.ModelSerializer):
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = InvoiceItem
        fields = [
            'id',
            'description',
            'quantity',
            'unit_price',
            'total'
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("La cantidad debe ser mayor a cero.")
        return value

    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio unitario no puede ser negativo.")
        return value


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, required=False)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    tax = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    number = serializers.CharField(read_only=True)

    class Meta:
        model = Invoice
        fields = [
            'id',
            'number',
            'customer',
            'status',
            'currency',
            'exchange_rate',
            'billing_address',
            'contact_email',
            'purchase_order_reference',
            'issued_date',
            'due_date',
            'subtotal',
            'tax',
            'total',
            'pdf_file',
            'sent_to_customer',
            'items'
        ]

    def validate(self, data):
        issued_date = data.get('issued_date')
        due_date = data.get('due_date')
        if issued_date and due_date and due_date < issued_date:
            raise serializers.ValidationError("La fecha de vencimiento no puede ser anterior a la fecha de emisión.")
        return data

    def validate_exchange_rate(self, value):
        if value <= 0:
            raise serializers.ValidationError("El tipo de cambio debe ser mayor que cero.")
        return value

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)
        invoice.recalculate_totals()
        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                InvoiceItem.objects.create(invoice=instance, **item_data)

        instance.recalculate_totals()
        return instance
