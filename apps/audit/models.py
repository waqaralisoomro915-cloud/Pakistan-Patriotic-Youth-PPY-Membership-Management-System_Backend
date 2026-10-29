import uuid
from django.db import models
from ..accounts.models import User

class Audit(models.Model):
    """Records important actions performed in the PPY system."""
    class Action(models.TextChoices):
        APPROVED = "approved", "Approved"
        REJECTED = "rejected", "Rejected"
        VERIFIED = "verified", "Verified"
        PENDING = "pending", "Pending"
        CREATED = "created", "Created"
        UPDATED = "updated", "Updated"
        DELETED = "deleted", "Deleted"
        RESUBMISSION_REQUESTED = (
            "resubmission_requested",
            "Resubmission Requested",
        )

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False, )
    actor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="audit_events",
        help_text="User who performed the action; empty for system actions.", )

    action = models.CharField(max_length=30,choices=Action.choices,help_text="Action recorded by the audit event.",)
    target_type = models.CharField(max_length=100,help_text="Type of record affected, e.g. Memberships or Verification.",)
    target_id = models.CharField(max_length=100,help_text="ID of the affected record.", )
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True,)
    details = models.JSONField(default=dict,blank=True,help_text="Additional structured information about the action.",)
    ip_address = models.GenericIPAddressField(null=True,blank=True,help_text="Client IP address, when available.",)
    class Meta:
        db_table = "audit"
        ordering = ["-timestamp"]
        verbose_name = "Audit Event"
        verbose_name_plural = "Audit Events"
    def __str__(self):
        return ( f"{self.action} - {self.target_type} "f"({self.target_id})",)
