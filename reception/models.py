from django.db import models
from django.core.validators import MinValueValidator

class CallType(models.TextChoices):
    RECEIVED = 'RECEIVED', 'Received'
    CANCELED = 'CANCELED', 'Canceled'
    IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
    COMPLETED = 'COMPLETED', 'Completed'
    PENDING = 'PENDING', 'Pending'

class Status(models.TextChoices):
    IN_CHECK = 'IN_CHECK', 'In Check'
    CHECK_FEEDBACK = 'CHECK_FEEDBACK', 'Check Feedback'
    CUSTOMER_CALL = 'CUSTOMER_CALL', 'Customer Call'
    IN_MAINTENANCE = 'IN_MAINTENANCE', 'In Maintenance'
    REFUSED = 'REFUSED', 'Refused'
    ACCEPTED = 'ACCEPTED', 'Accepted'
    WAIT_IN_RECEPTION = 'WAIT_IN_RECEPTION', 'Wait In Reception'
    GIVEN_TO_CUSTOMER = 'GIVEN_TO_CUSTOMER', 'Given To Customer'

class Place(models.TextChoices):
    RECEPTION = 'reception', 'Reception'
    MAINTENANCE = 'maintenance', 'Maintenance'
    CUSTOMER = 'customer', 'Customer'
    WAREHOUSE = 'warehouse', 'Warehouse'
    SHIPPING = 'shipping', 'Shipping'

class Reception(models.Model):
    reception_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name='customer')
    machine_id = models.ForeignKey('machine.Machine', on_delete=models.CASCADE, related_name='machine')
    receptionist_id = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='receptionist')
    check_machine_eng_id = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='check_machine_eng')
    maintenance_eng_id = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='maintenance_eng')
    given_to_customer_receptionist_id = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='given_to_customer_receptionist')
    case_number = models.CharField(max_length=255, unique=True)
    initial_damage = models.TextField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    initial_tax = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    initial_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_CHECK,
    )
    current_place = models.CharField(
        max_length=20,
        choices=Place.choices,
        default=Place.RECEPTION,
    )
    returned = models.BooleanField(default=False)
    who_received = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='receptionist_received', blank=True, null=True)  # Changed related_name to avoid conflict
    have_guarantee = models.BooleanField(default=False)
    in_guarantee = models.BooleanField(default=False)
    warranty_expiration_date = models.DateTimeField(blank=True, null=True)
    check_machine_date = models.DateTimeField(blank=True, null=True)
    check_feedback_date = models.DateTimeField(blank=True, null=True)
    check_feedback_description = models.TextField(max_length=500, blank=True, null=True)
    refused_reason = models.TextField(max_length=500, blank=True, null=True)
    refused_date = models.DateTimeField(blank=True, null=True)
    maintenance_date = models.DateTimeField(blank=True, null=True)
    excepted_completion_date = models.DateField(blank=True, null=True)
    given_to_customer_date = models.DateTimeField(blank=True, null=True)
    customer_notes = models.TextField(max_length=500, blank=True, null=True)
    priority = models.SmallIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return f"Reception {self.reception_id} - {self.customer_id.customer_name} - {self.machine_id.machine_type_id.machine_name}"

class Call(models.Model):
    call_id = models.AutoField(primary_key=True)
    call_type = models.CharField(
        max_length=20,
        choices=CallType.choices,
        default=CallType.RECEIVED,
    )
    summary = models.TextField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(max_length=500, blank=True, null=True)
    reception_id = models.ForeignKey('Reception', on_delete=models.CASCADE, related_name='call')
    caller_id = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='caller')

    def __str__(self):
        return f"Call {self.call_id} - {self.reception_id.reception_id} - {self.call_type}"

class ReceptionPhoto(models.Model):
    reception_photo_id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey('Reception', on_delete=models.CASCADE, related_name='reception_photos')
    photo = models.ImageField(upload_to='reception_photos/')
    date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"Photo {self.reception_photo_id} - Reception {self.reception_id.reception_id}"

class RepairNote(models.Model):
    repair_note_id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey('Reception', on_delete=models.CASCADE, related_name='repair_notes')
    date = models.DateTimeField(auto_now_add=True)
    note = models.TextField(max_length=500, blank=True, null=True)
    technician_id = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='technician')

    def __str__(self):
        return f"Repair Note {self.repair_note_id} - Reception {self.reception_id.reception_id}"

class StatusChange(models.Model):
    status_change_id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey('Reception', on_delete=models.CASCADE, related_name='status_changes')
    date = models.DateTimeField(auto_now_add=True)
    old_status = models.CharField(max_length=20, choices=Status.choices)
    new_status = models.CharField(max_length=20, choices=Status.choices)
    user_id = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='user')

    def __str__(self):
        return f"Status Change {self.status_change_id} - Reception {self.reception_id.reception_id}"