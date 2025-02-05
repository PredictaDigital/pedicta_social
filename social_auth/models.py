from django.db import models

class AuthProvider(models.TextChoices):
    GOOGLE = "google", "Google"
    INSTAGRAM = "instagram", "Instagram"
    FACEBOOK = "facebook", "Facebook"
    LINKEDIN = "linkedin", "LinkedIn"

class SocialAuthToken(models.Model):
    email = models.EmailField(unique=True)
    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    expires_in = models.IntegerField(help_text="Expiration time in seconds", null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    provider = models.CharField(
        max_length=10,
        choices=AuthProvider.choices,
        default=AuthProvider.GOOGLE,
    )

    class Meta:
        db_table = "auth_token"

    def __str__(self):
        return f"{self.email} ({self.provider})"
