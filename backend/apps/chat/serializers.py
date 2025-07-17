from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()

class ChatRoomSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all()
    )

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'is_group', 'members', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        members = data.get('members', [])
        is_group = data.get('is_group', False)

        if not members or len(members) == 0:
            raise serializers.ValidationError('Debe haber al menos un miembro en la sala.')

        if is_group and len(members) < 2:
            raise serializers.ValidationError('Un chat grupal debe tener al menos dos miembros.')

        if not is_group and len(members) != 2:
            raise serializers.ValidationError('Un chat privado debe tener exactamente dos miembros.')

        return data

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    attachment = serializers.FileField(required=False, allow_null=True, use_url=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'room',
            'sender',
            'content',
            'message_type',
            'attachment',
            'created_at',
            'read_by',
        ]
        read_only_fields = ['created_at', 'read_by']

    def validate(self, data):
        message_type = data.get('message_type', 'text')
        content = data.get('content')
        attachment = data.get('attachment')

        if message_type == 'text' and (content is None or content.strip() == ''):
            raise serializers.ValidationError('El contenido del mensaje no puede estar vacío para mensajes de texto.')

        if message_type in ['image', 'file'] and attachment is None:
            raise serializers.ValidationError(f'Los mensajes de tipo {message_type} deben tener un archivo adjunto.')

        if message_type == 'system' and (content is None or content.strip() == ''):
            raise serializers.ValidationError('Los mensajes de sistema deben tener contenido.')

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['sender'] = request.user
        return super().create(validated_data)
