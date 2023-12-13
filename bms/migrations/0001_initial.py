# Generated by Django 4.2.1 on 2023-06-08 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='busRoute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),

        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('vehicle_number', models.CharField(max_length=15)),
                ('source', models.CharField(max_length=50, null=True)),
                ('destination', models.CharField(max_length=50, null=True)),
                ('v_status', models.BooleanField(default=True)),
                ('departure', models.TimeField(blank=True, null=True)),
                ('arrive', models.TimeField(blank=True, null=True)),
                ('total_seats', models.IntegerField(default=0)),
                ('booked_seats', models.IntegerField(default=0)),
                ('price', models.IntegerField(default=0)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-updated', '-created'],
            },
        ),
    ]
