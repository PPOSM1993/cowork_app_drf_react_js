# Generated by Django 4.2.23 on 2025-07-16 17:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('notification_type', models.CharField(choices=[('system', 'System'), ('reservation', 'Reservation'), ('payment', 'Payment'), ('support', 'Support'), ('promotion', 'Promotion'), ('general', 'General')], default='system', max_length=20)),
                ('delivery_method', models.CharField(choices=[('internal', 'Internal'), ('email', 'Email'), ('push', 'Push'), ('sms', 'SMS')], default='internal', max_length=20)),
                ('is_read', models.BooleanField(default=False)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('related_object_type', models.CharField(blank=True, max_length=100, null=True)),
                ('related_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-sent_at'],
            },
        ),
    ]
