from django.db import models
import uuid
# Create your models here.

class UserData(models.Model):
    full_name=models.CharField(max_length=150)
    address=models.TextField(null=True,blank=True)
    emergency_contact1=models.IntegerField(max_length=10, null=True, blank=True)
    emergency_contact2=models.IntegerField(max_length=10, null=True, blank=True)
    unique_id = models.UUIDField(editable=False, unique=True, default=uuid.uuid4)
    # qr_code = models.ImageField(upload_to='qr_codes/',null=True,blank=True)
