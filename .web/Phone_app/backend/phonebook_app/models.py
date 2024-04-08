from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="First Name")
    surname = models.CharField(max_length=100, verbose_name="Last Name")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Person"
        verbose_name_plural = "People"

    def __str__(self):
        return f"{self.name} {self.surname}"


class PhoneNumber(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="phone_numbers",
        verbose_name="Person",
    )
    number = models.CharField(max_length=20, unique=True, verbose_name="Phone Number")
    country_code = models.CharField(max_length=5, verbose_name="Country Code")
    is_primary = models.BooleanField(default=False, verbose_name="Primary")

    class Meta:
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"
        constraints = [
            models.UniqueConstraint(
                fields=["person", "is_primary"], name="unique_primary_phone_number"
            ),
        ]

    def clean(self):

        if self.is_primary:
            existing_primary = (
                PhoneNumber.objects.filter(person=self.person, is_primary=True)
                .exclude(pk=self.pk)
                .exists()
            )
            if existing_primary:
                raise ValidationError(
                    "У человека может быть только один основной номер телефона."
                )

    def __str__(self):
        is_primary = "Primary" if self.is_primary else ""
        return f"{self.country_code} {self.number} ({is_primary})"


@receiver(post_save, sender=PhoneNumber)
def set_primary_phone(sender, instance, created, **kwargs):
    if created:
        # Check if this is the first phone number for this person
        existing_primary = PhoneNumber.objects.filter(
            person=instance.person, is_primary=True
        ).exists()

        # If it's the first phone number, set it as primary
        if not existing_primary:
            instance.is_primary = True
            instance.save(update_fields=["is_primary"])
