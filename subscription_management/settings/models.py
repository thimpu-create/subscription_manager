from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class SMTPSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    host = models.CharField(max_length=255)
    port = models.IntegerField()
    password = models.CharField(max_length=255)
    use_ssl = models.BooleanField(default=False)
    use_tls = models.BooleanField(default=True)
    email = models.EmailField()

    class Meta:
        verbose_name = 'SMTP Settings'
        verbose_name_plural = 'SMTP Settings'

    def __str__(self):
        return f"SMTP Settings for {self.user.email}"