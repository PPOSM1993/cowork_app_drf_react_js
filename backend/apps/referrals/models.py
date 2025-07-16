from django.db import models
from django.conf import settings

class Referral(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('registered', 'Registered'),
        ('rewarded', 'Rewarded'),
        ('cancelled', 'Cancelled'),
    ]

    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='sent_referrals',
        on_delete=models.CASCADE
    )
    referred_email = models.EmailField()
    referred_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='received_referrals',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    referral_code = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reward_granted = models.BooleanField(default=False)
    reward_description = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.referrer.email} → {self.referred_email} ({self.status})"