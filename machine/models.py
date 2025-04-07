from django.db import models

# Create your models here.
class MachineType(models.Model):
    machine_id = models.AutoField(primary_key=True)
    machine_name = models.CharField(max_length=100, unique=True)
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE, related_name='machine_types')
    def __str__(self):
        return self.machine_type_name
    
class Machine(models.Model):
    machine_id = models.AutoField(primary_key=True)
    machine_type = models.ForeignKey('MachineType', on_delete=models.CASCADE, related_name='machines')
    model_num = models.CharField(max_length=100, blank=True, null=True)
    serial_num = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.machine_type.name} ({self.serial_num})"

class MultiReceptionAndTV(models.Model):
    id = models.AutoField(primary_key=True)
    reception_id = models.ForeignKey('reception.Reception', on_delete=models.CASCADE, related_name='multi_reception_and_tv')
    machine_id = models.ForeignKey('Machine', on_delete=models.CASCADE, related_name='multi_reception_and_tv')

class Agent(models.Model):
    agent_id = models.AutoField(primary_key=True)
    agent_name = models.CharField(max_length=100)

    def __str__(self):
        return self.agent_name