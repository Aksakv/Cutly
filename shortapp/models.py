from django.db import models

# Create your models here.
class URLModel(models.Model):
    long_url = models.URLField()
    short_code = models.CharField(max_length=30,unique=True)
    clicks = models.IntegerField(default=0)
    def __str__(self):
        return self.long_url