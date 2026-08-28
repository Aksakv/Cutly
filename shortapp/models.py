
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from django.conf import settings


class URLModel(models.Model):
    long_url = models.URLField()
    short_code = models.CharField(max_length=30, unique=True)
    clicks = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    qr_code = models.ImageField(
        upload_to="qr_codes/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.long_url

    def save(self, *args, **kwargs):
        # Save the object first so it gets an ID
        super().save(*args, **kwargs)

        # Generate QR code only if one doesn't already exist
        if not self.qr_code:
            site_url = getattr(
                settings,
                "SITE_URL",
                "http://127.0.0.1:8000"
            ).rstrip("/")

            short_url = f"{site_url}/{self.short_code}"

            qr = qrcode.make(short_url)

            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            buffer.seek(0)

            file_name = f"{self.short_code}.png"

            self.qr_code.save(
                file_name,
                File(buffer),
                save=False
            )

            super().save(update_fields=["qr_code"])


class ClickEvent(models.Model):
    url = models.ForeignKey(
        URLModel,
        on_delete=models.CASCADE
    )
    timestamp = models.DateTimeField(auto_now_add=True)
