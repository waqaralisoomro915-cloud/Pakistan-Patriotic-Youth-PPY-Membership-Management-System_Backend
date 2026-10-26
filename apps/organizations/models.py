
import uuid
from django.core.exceptions import ValidationError
from django.db import models

class Organization(models.Model):

    class Level(models.TextChoices):
        NATIONAL = "national", "National"
        PROVINCE = "province", "Province"
        DISTRICT = "district", "District"
        TEHSIL = "tehsil", "Tehsil"

    # Unique identifier for each organization
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False, )
    # Basic organization information
    name = models.CharField(max_length=150)

    code = models.SlugField(max_length=100,unique=True,)

    level = models.CharField(max_length=20,choices=Level.choices,)

    description = models.TextField(blank=True)

    # Connects this organization to its parent
    parent = models.ForeignKey("self",on_delete=models.PROTECT,related_name="children",null=True,blank=True,)

    # Organization status
    is_active = models.BooleanField(default=True)
    # Record timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["level", "name"]
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def clean(self):
        """Validate parent and child organization relationships."""

        super().clean()

        if self.parent_id and self.parent:
            if self.pk and self.parent_id == self.pk:
                raise ValidationError({
                    "parent": "An organization cannot be its own parent."
                })

            expected_parent_levels = {
                self.Level.NATIONAL: None,
                self.Level.PROVINCE: self.Level.NATIONAL,
                self.Level.DISTRICT: self.Level.PROVINCE,
                self.Level.TEHSIL: self.Level.DISTRICT,
            }

            expected_parent_level = expected_parent_levels[self.level]

            if expected_parent_level is None:
                raise ValidationError({
                    "parent": "The National organization cannot have a parent."
                })

            if self.parent.level != expected_parent_level:
                raise ValidationError({
                    "parent": (
                        f"A {self.get_level_display()} organization "
                        f"must belong to a "
                        f"{self.Level(expected_parent_level).label} organization."
                    )
                })

        elif self.level != self.Level.NATIONAL:
            raise ValidationError({
                "parent": (
                    f"A {self.get_level_display()} organization "
                    "must have a parent."
                )
            })

    def __str__(self):
        return f"{self.name} ({self.get_level_display()})"
