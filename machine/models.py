from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Agent(models.Model):
    agent_id = models.AutoField(primary_key=True)
    agent_name = models.CharField(
        max_length=100,
        unique=True,  # Ensure agent names are unique
        validators=[MinLengthValidator(2, _("Agent name must be at least 2 characters."))],
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Track creation time

    class Meta:
        ordering = ['agent_name']  # Default ordering by name
        verbose_name = "Agent"
        verbose_name_plural = "Agents"

    def __str__(self):
        return self.agent_name


class MachineType(models.Model):
    machine_type_id = models.AutoField(primary_key=True)
    machine_name = models.CharField(max_length=100, unique=True)
    agent = models.ForeignKey('Agent', on_delete=models.CASCADE, related_name='machine_types')


class MachineModel(models.Model):
    model_id = models.AutoField(primary_key=True)
    model_name = models.CharField(
        max_length=100,
        unique=True,
        validators=[MinLengthValidator(2, _("Model name must be at least 2 characters."))]
    )
    machine_type = models.ForeignKey(  # Renamed for clarity
        'MachineType',
        on_delete=models.CASCADE,
        related_name='machine_models'
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Track creation time

    class Meta:
        ordering = ['model_name']
        verbose_name = "Machine Model"

    def __str__(self):
        return self.model_name


class Machine(models.Model):
    machine_id = models.AutoField(primary_key=True)
    machine_type = models.ForeignKey(  # Renamed for clarity
        'MachineType',
        on_delete=models.CASCADE,
        related_name='machines'
    )
    model = models.ForeignKey(  # Renamed for clarity
        'MachineModel',
        on_delete=models.CASCADE,
        related_name='machines'
    )
    serial_num = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        unique=True,  # Ensure serial numbers are unique when provided
        help_text=_("Unique serial number for the machine (optional).")
    )
    manufactured_date = models.DateField(blank=True, null=True)  # Optional field for tracking

    class Meta:
        ordering = ['machine_type__machine_name', 'serial_num']
        verbose_name = "Machine"

    def __str__(self):
        serial = self.serial_num if self.serial_num else "No Serial"
        return f"{self.machine_type.machine_name} - {self.model.model_name} ({serial})"


class MultiReceptionAndTV(models.Model):
    id = models.AutoField(primary_key=True)
    reception = models.ForeignKey(  # Renamed for clarity
        'reception.Reception',
        on_delete=models.CASCADE,
        related_name='multi_reception_and_tv'
    )
    machine = models.ForeignKey(  # Renamed for clarity
        'Machine',
        on_delete=models.CASCADE,
        related_name='multi_reception_and_tv'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)  # Track assignment time

    class Meta:
        verbose_name = "Multi Reception and TV"
        verbose_name_plural = "Multi Receptions and TVs"
        unique_together = [['reception', 'machine']]  # Prevent duplicate assignments

    def __str__(self):
        return f"{self.machine} assigned to {self.reception}"