from django.db import models
from django.conf import settings

class ChatRoom(models.Model):
    """
    Representa una sala o canal de chat.
    Puede ser privado (2 personas) o grupal.
    """
    name = models.CharField(max_length=255, blank=True, null=True, help_text='Nombre para chats grupales')
    is_group = models.BooleanField(default=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_group:
            return self.name or f'Grupo {self.pk}'
        else:
            return f'Chat privado {self.pk}'

class Message(models.Model):
    """
    Mensajes enviados en las salas de chat.
    """
    MESSAGE_TYPES = [
        ('text', 'Texto'),
        ('image', 'Imagen'),
        ('file', 'Archivo'),
        ('system', 'Sistema'),
    ]

    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='sent_messages')
    content = models.TextField(blank=True, null=True)
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default='text')
    attachment = models.FileField(upload_to='chat_attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='read_messages', blank=True)

    def __str__(self):
        return f'Mensaje {self.pk} en sala {self.room.pk}'

    class Meta:
        ordering = ['created_at']
