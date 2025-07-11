# Generated by Django 4.2.21 on 2025-06-18 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('icon', models.CharField(blank=True, help_text='Icono o clase CSS', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('image', models.ImageField(blank=True, null=True, upload_to='branches/')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(choices=[('shared', 'Espacio Compartido'), ('private', 'Oficina Privada'), ('meeting', 'Sala de Reuniones'), ('event', 'Espacio para Eventos')], default='shared', max_length=20)),
                ('capacity', models.PositiveIntegerField(help_text='Máximo de personas')),
                ('price_per_hour', models.DecimalField(decimal_places=2, max_digits=8)),
                ('price_per_day', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('price_per_month', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('max_simultaneous_reservations', models.PositiveIntegerField(default=1)),
                ('latitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='spaces/')),
                ('rules', models.TextField(blank=True, help_text='Reglas o políticas del espacio', null=True)),
                ('cancellation_policy', models.TextField(blank=True, help_text='Política de cancelación', null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('access_24_7', models.BooleanField(default=False)),
                ('accessible_for_disabled', models.BooleanField(default=False)),
                ('has_special_equipment', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('amenities', models.ManyToManyField(blank=True, to='spaces.amenity')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spaces', to='spaces.branch')),
                ('tags', models.ManyToManyField(blank=True, to='spaces.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.PositiveSmallIntegerField(choices=[(0, 'Lunes'), (1, 'Martes'), (2, 'Miércoles'), (3, 'Jueves'), (4, 'Viernes'), (5, 'Sábado'), (6, 'Domingo')])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('space', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availabilities', to='spaces.space')),
            ],
            options={
                'unique_together': {('space', 'day_of_week', 'start_time', 'end_time')},
            },
        ),
    ]
