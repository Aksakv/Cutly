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
    qr_code = models.ImageField(upload_to='qr_code/',blank=True,null=True)
    def __str__(self):
        return self.long_url
    def save(self,*args,**kwargs):
        short_url =f"{settings.SITE_URL}/{self.short_code}"
        qr = qrcode.make(short_url)
        bufer =BytesIO()
        qr.save(bufer,format=
                'PNG')
        file_name = f"{self.short_code}.png"
        self.qr_code.save(file_name,File(bufer),save =False)
        super().save(*args,**kwargs)
