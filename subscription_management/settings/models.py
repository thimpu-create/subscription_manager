from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from .utils import encrypt_password, decrypt_password  # Import from your utils

class SMTPSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    password = models.CharField(max_length=255)  # This will store encrypted password
    use_ssl = models.BooleanField(default=False)
    use_tls = models.BooleanField(default=True)
    email = models.EmailField()

    def save(self, *args, **kwargs):
        if not self.password.startswith('gAAAA'):  # Fernet-encrypted strings start with this
            self.password = encrypt_password(self.password)
        super().save(*args, **kwargs)

    @property
    def decrypted_password(self):
        try:
            return decrypt_password(self.password)
        except Exception:
            return ''  # fallback or raise exception if needed

    class Meta:
        verbose_name = 'SMTP Settings'
        verbose_name_plural = 'SMTP Settings'

    def __str__(self):
        return f"SMTP Settings for {self.user.email}"