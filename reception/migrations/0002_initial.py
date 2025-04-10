# Generated by Django 5.1.7 on 2025-04-10 01:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer', '0002_initial'),
        ('machine', '0002_initial'),
        ('reception', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='caller_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caller', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reception',
            name='check_machine_eng_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='check_machine_eng', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reception',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='customer.customer'),
        ),
        migrations.AddField(
            model_name='reception',
            name='given_to_customer_receptionist_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='given_to_customer_receptionist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reception',
            name='machine_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='machine', to='machine.machine'),
        ),
        migrations.AddField(
            model_name='reception',
            name='maintenance_eng_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_eng', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reception',
            name='receptionist_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receptionist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reception',
            name='who_received',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receptionist_received', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='call',
            name='reception_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='call', to='reception.reception'),
        ),
        migrations.AddField(
            model_name='receptionphoto',
            name='reception_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reception_photos', to='reception.reception'),
        ),
        migrations.AddField(
            model_name='repairnote',
            name='reception_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='repair_notes', to='reception.reception'),
        ),
        migrations.AddField(
            model_name='repairnote',
            name='technician_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='technician', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='statuschange',
            name='reception_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='status_changes', to='reception.reception'),
        ),
        migrations.AddField(
            model_name='statuschange',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
