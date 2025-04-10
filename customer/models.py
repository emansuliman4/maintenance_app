from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=100) # not dropdown list
    customer_email = models.EmailField(max_length=100, unique=True)
    customer_city = models.TextField(max_length=50, blank=True, null=True)
    customer_address = models.TextField(max_length=100, blank=True, null=True)
    Date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='customer_created_by')
    created_at = models.DateTimeField(auto_now_add=True)# LOOK
    blocked = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name
    
class CustomerPhone(models.Model):
    customer_phone_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='customer_phones')
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.phone_number