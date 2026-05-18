from django.db import models


class School(models.Model):
    """Tenant root — each Islamic school on the platform."""

    STATUS_ACTIVE = 'active'
    STATUS_SUSPENDED = 'suspended'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_SUSPENDED, 'Suspended'),
    ]

    TIER_FREE = 'free'
    TIER_STANDARD = 'standard'
    TIER_PREMIUM = 'premium'
    TIER_CHOICES = [
        (TIER_FREE, 'Free'),
        (TIER_STANDARD, 'Standard'),
        (TIER_PREMIUM, 'Premium'),
    ]

    name = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True)
    subscription_tier = models.CharField(
        max_length=20, choices=TIER_CHOICES, default=TIER_FREE,
    )
    # stripe connect account id once school finishes onboarding
    stripe_account_id = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
