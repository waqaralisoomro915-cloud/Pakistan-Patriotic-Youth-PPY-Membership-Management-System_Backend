import uuid
from django.db import models
from django.utils import timezone
from ..memberships.models import Memberships
from ..positions.models import Positions
from ..organizations.models import Organization


class Card(models.Model):

    class CardType(models.TextChoices):
        MEMBERSHIP_CARD = "membership_card", "Membership Card"
        LEADERSHIP_CARD = "leadership_card", "Leadership Card"

    class CardStatus(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        EXPIRED = "expired", "Expired"
        REPLACED = "replaced", "Replaced"
        REVOKED = "revoked", "Revoked"

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,)
    membership = models.ForeignKey( Memberships,on_delete=models.PROTECT,related_name="cards",)
    card_number = models.CharField(max_length=30,unique=True,)
    card_type = models.CharField( max_length=20,choices=CardType.choices,)
    position = models.ForeignKey(Positions,on_delete=models.PROTECT,null=True, blank=True, related_name="cards",)
    organization = models.ForeignKey( Organization,on_delete=models.PROTECT,related_name="cards",)
    issued_at = models.DateTimeField( default=timezone.now, )
    expiration_date = models.DateTimeField(null=True,blank=True,)
    status = models.CharField( max_length=10, choices=CardStatus.choices, default=CardStatus.ACTIVE,)
    created_at = models.DateTimeField(auto_now_add=True,)
    updated_at = models.DateTimeField(auto_now=True,)
    class Meta:
        db_table = "card"
        verbose_name = "Card"
        verbose_name_plural = "Cards"
        ordering = ["-created_at"]

    def __str__(self):
        return self.card_number
