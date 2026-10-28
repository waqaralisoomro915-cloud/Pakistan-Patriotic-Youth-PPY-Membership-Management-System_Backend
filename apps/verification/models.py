
import uuid
from django.db import models

from ..accounts.models import User
from ..memberships.models import Memberships
class Verification(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        RESUBMISSION_REQUIRED = ("resubmission_required","Resubmission Required",)
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,)
    membership = models.OneToOneField(Memberships, on_delete=models.PROTECT,related_name="verification",)
    identity_document = models.FileField(upload_to="identity_documents/",)
    police_verification_certificate = models.FileField( upload_to="police_verification_certificates/",)
    status = models.CharField(max_length=25,choices=Status.choices,default=Status.PENDING,)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey( User,on_delete=models.SET_NULL, null=True,blank=True,related_name="verifications_reviewed", )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    review_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "verification"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Verification: {self.membership} - {self.status}"
