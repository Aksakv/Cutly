from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings

# Create your models here.
class URLModel(models.Model):
    long_url = models.URLField()
    short_code = models.CharField(max_length=30,unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(upload_to='qr_codes/',blank=True,null=True)
    def __str__(self):
        return self.long_url

    def save(self, *args, **kwargs):
        # Step 1: Save first
        super().save(*args, **kwargs)

        # Step 2: Only create QR if not exists
        if not self.qr_code:
            short_url = f"http://127.0.0.1:8000/{self.short_code}"

            qr = qrcode.make(short_url)
            buffer = BytesIO()
            qr.save(buffer, format='PNG')

            file_name = f"{self.short_code}.png"

            self.qr_code.save(file_name, File(buffer), save=False)

            # Step 3: Save again
            super().save(update_fields=['qr_code'])
class ClickEvent(models.Model):
    url = models.ForeignKey(URLModel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
