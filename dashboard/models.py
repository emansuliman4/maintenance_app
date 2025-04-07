from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL

class ProcessMaintenance(models.Model):
    process_maintenance_id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey(
        'Reception',
        on_delete=models.CASCADE,
        related_name='process_maintenances'
    )
    eng_name = models.CharField(max_length=100, blank=True, null=True)
    damage = models.TextField(max_length=500, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

class ProcessToReception(models.Model):
    process_to_reception_id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey(
        'Reception',
        on_delete=models.CASCADE,
        related_name='process_to_receptions'
    )
    who_received = models.CharField(max_length=100, blank=True, null=True)
    current_place = models.CharField(max_length=100, blank=True, null=True)

class Reception(models.Model):
    reception_id = models.AutoField(primary_key=True)
    case_number = models.ForeignKey(
        'machine.Machine',
        on_delete=models.CASCADE,
        related_name='dashboard_receptions'
    )
    initial_damage = models.TextField(max_length=500, blank=True, null=True)
    real_damage = models.TextField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    who_received = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use Django's built-in User model
        on_delete=models.CASCADE,
        related_name='received_receptions'
    )
    received = models.BooleanField(default=False)
    replay = models.TextField(max_length=500, blank=True, null=True)
    check_feedback = models.TextField(max_length=500, blank=True, null=True)
    calling_customer = models.BooleanField(default=False)
    given_to_customer = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_place = models.CharField(max_length=100, blank=True, null=True)
    process_maintenance = models.ForeignKey(
        'ProcessMaintenance',
        on_delete=models.CASCADE,
        related_name='receptions',
        blank=True,
        null=True
    )
    process_to_reception = models.ForeignKey(
        'ProcessToReception',
        on_delete=models.CASCADE,
        related_name='receptions',
        blank=True,
        null=True
    )
    attachments = models.FileField(upload_to='attachments/%Y-%m-%d/', blank=True, null=True)
    receptionists = models.CharField(max_length=100, blank=True, null=True)
    machines = models.CharField(max_length=100, blank=True, null=True)
    calls = models.CharField(max_length=100, blank=True, null=True)