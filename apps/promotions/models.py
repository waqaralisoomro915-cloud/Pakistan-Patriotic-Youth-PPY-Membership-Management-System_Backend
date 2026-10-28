import uuid
from django.db import models
from ..accounts.models import User
from ..memberships.models import Memberships
from ..positions.models import Positions


class Promotions(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,)
    membership = models.ForeignKey(Memberships,on_delete=models.PROTECT,related_name="promotions",)
    current_position = models.ForeignKey(Positions,on_delete=models.PROTECT,related_name="current_promotions",null=True,blank=True,)
    requested_position = models.ForeignKey(Positions,on_delete=models.PROTECT,related_name="requested_promotions",)
    status = models.CharField(max_length=10,choices=Status.choices,default=Status.PENDING,)
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="promotions_reviewed",null=True,blank=True,)
    reviewed_at = models.DateTimeField(null=True,blank=True,)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "promotions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.membership} - {self.requested_position}"


