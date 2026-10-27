import uuid
from django.db import models
from ..accounts.models import User
from ..organizations.models import Organization
class Memberships(models.Model):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        SUSPENDED = "suspended", "Suspended"
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,)
    user = models.ForeignKey( User,on_delete=models.CASCADE,related_name="memberships" )
    organization = models.ForeignKey(Organization,on_delete=models.PROTECT,related_name="memberships",)
    membership_number = models.CharField(max_length=20,unique=True,null=True,blank=True,)
    status = models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING,)
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name="memberships_reviewed",)
    reviewed_at = models.DateTimeField(null=True,blank=True,)
    rejection_reason = models.TextField(blank=True)
    joined_at = models.DateTimeField(null=True,blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "memberships"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.status}"
