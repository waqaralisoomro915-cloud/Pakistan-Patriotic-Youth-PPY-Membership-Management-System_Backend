
import uuid
from django.db import models
from ..organizations.models import Organization


class Positions(models.Model):

    class Level(models.TextChoices):
        NATIONAL = "national", "National"
        PROVINCE = "province", "Province"
        DISTRICT = "district", "District"
        TEHSIL = "tehsil", "Tehsil"

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,)

    name = models.CharField(max_length=200)
    code = models.SlugField(max_length=200)
    level = models.CharField(max_length=20, choices=Level.choices)
    description = models.TextField(blank=True)
    organization = models.ForeignKey(Organization,on_delete=models.PROTECT,related_name="positions",)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "positions"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "code"],
                name="unique_position_code_per_org",
            ),
        ]
        indexes = [
            models.Index(
                fields=["organization", "code"],
                name="position_org_code_idx",
            ),]

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
