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
    qr_code = models.ImageField(upload_to='qr_code/',blank=True,null=True)
    def __str__(self):
        return self.long_url
    def save(self,*args,**kwargs):
        short_url =f"{settings.SITE_URL}/{self.short_code}"
        qr = qrcode.make(short_url)
        buffer =BytesIO()
        qr.save(buffer,format='PNG')
        buffer.seek(0)
        file_name = f"{self.short_code}.png"
        self.qr_code.save(file_name,File(buffer),save =False)
        super().save(*args,**kwargs)
class ClickEvent(models.Model):
    url = models.ForeignKey(URLModel, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
