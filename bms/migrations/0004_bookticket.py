# Generated by Django 4.2.1 on 2023-07-26 08:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bms', '0003_passenger_vehicle'),
    ]

    operations = [
        migrations.CreateModel(
            name='bookTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_ticket', models.IntegerField(default=0)),
                ('ticketNumber', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicleid', to='bms.vehicle')),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
    ]
