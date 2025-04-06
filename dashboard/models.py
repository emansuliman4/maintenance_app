from django.db import models

# Create your models here.
class ProcessMaintenance(models.Model):
    process_maintenance_id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey('Reception', on_delete=models.CASCADE, related_name='process_maintenance')
    eng_name = models.CharField(max_length=100, blank=True, null=True)  # Dropdown in forms
    damage = models.TextField(max_length=500, blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

class ProcessToReception(models.Model):
    process_to_reception_id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey('Reception', on_delete=models.CASCADE, related_name='process_to_reception')
    who_received = models.CharField(max_length=100, blank=True, null=True)  # Dropdown in forms
    current_place = models.CharField(max_length=100, blank=True, null=True)  # Dropdown in forms

class Reception:
    reception_id = models.AutoField(primary_key=True)
    case_number = models.ForeignKey('machine.Machine', on_delete=models.CASCADE, related_name='receptions')
    initial_damage = models.TextField(max_length=500, blank=True, null=True)
    real_damage = models.TextField(max_length=500, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    who_received = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='received_receptions') #Dropdown in forms
    received = models.BooleanField(default=False) # if false, text info
    replay = models.TextField(max_length=500, blank=True, null=True) 
    check_feedback = models.TextField(max_length=500, blank=True, null=True)
    calling_customer = models.BooleanField(default=False)
    given_to_customer = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_place = models.CharField(max_length=100, blank=True, null=True) #Dropdown in forms
# relationships
    process_maintenance = models.ForeignKey('ProcessMaintenance', on_delete=models.CASCADE, related_name='process_maintenance', blank=True, null=True)
    process_to_reception = models.ForeignKey('ProcessToReception', on_delete=models.CASCADE, related_name='process_to_reception', blank=True, null=True)
    attachments = models.FileField(upload_to='attachments/%Y-%m-%d/', blank=True, null=True)
    receptionists = models.CharField(max_length=100, blank=True, null=True) #Dropdown in forms
    machines = models.CharField(max_length=100, blank=True, null=True) #Dropdown in forms
    calls = models.CharField(max_length=100, blank=True, null=True) #Dropdown in forms