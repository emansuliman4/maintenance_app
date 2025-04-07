from django.db import models
from user.models import User 
from machine.models import Machine
# Create your models here.
class CallType(models.TextChoices):
    RECEIVED = 'received', 'Received'
    CANCELED = 'canceled', 'Canceled'

class Calls(models.Model):
    call_id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey('Reception', on_delete=models.CASCADE, related_name='calls')  # Links to Reception
    time = models.DateTimeField(auto_now_add=True)
    replay = models.TextField(max_length=500, blank=True, null=True)
    call_status = models.CharField(max_length=100, choices=CallType.choices, default=CallType.RECEIVED)

    def __str__(self):
        return str(self.call_id)

class Reception(models.Model):
    reception_id = models.AutoField(primary_key=True)
    initial_damage = models.TextField(max_length=500, blank=True, null=True)
    real_damage = models.TextField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    who_received = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='received_receptions')
    received = models.BooleanField(default=False)
    check_feedback = models.TextField(max_length=500, blank=True, null=True)
    calling_customer = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    process_stage = models.CharField(max_length=500, blank=True, null=True) # Dropdown in forms
    engineer_name = models.CharField(max_length=100, blank=True, null=True)  # Dropdown in forms
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    maintenance_time = models.DateTimeField(blank=True, null=True)
    current_place = models.CharField(max_length=100, blank=True, null=True)  # Dropdown in forms
    have_guarantee = models.BooleanField(default=True)
    guarantee = models.IntegerField(blank=True, null=True)
    case_number = models.ForeignKey('machine.Machine', on_delete=models.CASCADE, related_name='receptions')


    def __str__(self):
        return f"Reception {self.reception_id}"

class Attachment(models.Model):
    attachment_id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey('Reception', on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='attachments/%Y-%m-%d/')
    name = models.CharField(max_length=255, blank=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_type = models.CharField(max_length=50, blank=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.file.name
        if not self.file_type:
            self.file_type = self.file.name.split('.')[-1]  # Extract extension
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Receptionist(models.Model):
    Receptionist_id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey('Reception', on_delete=models.CASCADE, related_name='receptionist')
    receptionist_name = models.CharField(max_length=100)

class MultiReceptionAndCustomer:
    id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey('Reception', on_delete=models.CASCADE, related_name='multi_reception')
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, related_name='multi_customer')

# class ProcessCall:
#     call_id = models.AutoField(primary_key=True)
#     reception_id = models.ForeignKey('Reception', on_delete=models.CASCADE, related_name='process_call')
#     time = models.DateTimeField(auto_now_add=True)
#     replay = models.TextField(max_length=500, blank=True, null=True)