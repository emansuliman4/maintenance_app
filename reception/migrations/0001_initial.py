# Generated by Django 5.1.7 on 2025-04-07 12:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('machine', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('attachment_id', models.AutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(upload_to='attachments/%Y-%m-%d/')),
                ('name', models.CharField(blank=True, max_length=255)),
                ('upload_date', models.DateTimeField(auto_now_add=True)),
                ('file_type', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Calls',
            fields=[
                ('call_id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('replay', models.TextField(blank=True, max_length=500, null=True)),
                ('call_status', models.CharField(choices=[('received', 'Received'), ('canceled', 'Canceled')], default='received', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Receptionist',
            fields=[
                ('Receptionist_id', models.AutoField(primary_key=True, serialize=False)),
                ('receptionist_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reception',
            fields=[
                ('reception_id', models.AutoField(primary_key=True, serialize=False)),
                ('initial_damage', models.TextField(blank=True, max_length=500, null=True)),
                ('real_damage', models.TextField(blank=True, max_length=500, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('received', models.BooleanField(default=False)),
                ('check_feedback', models.TextField(blank=True, max_length=500, null=True)),
                ('calling_customer', models.BooleanField(default=False)),
                ('accepted', models.BooleanField(default=False)),
                ('process_stage', models.CharField(blank=True, max_length=500, null=True)),
                ('engineer_name', models.CharField(blank=True, max_length=100, null=True)),
                ('cost', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('maintenance_time', models.DateTimeField(blank=True, null=True)),
                ('current_place', models.CharField(blank=True, max_length=100, null=True)),
                ('have_guarantee', models.BooleanField(default=True)),
                ('guarantee', models.IntegerField(blank=True, null=True)),
                ('case_number', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receptions', to='machine.machine')),
            ],
        ),
    ]
