from cryptography.fernet import Fernet
from django.conf import settings

def encrypt_password(raw_password):
    f = Fernet(settings.EMAIL_ENCRYPTION_KEY)
    return f.encrypt(raw_password.encode()).decode()

def decrypt_password(encrypted_password):
    f = Fernet(settings.EMAIL_ENCRYPTION_KEY)
    return f.decrypt(encrypted_password.encode()).decode()