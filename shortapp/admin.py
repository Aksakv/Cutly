from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(URLModel)
admin.site.register(ClickEvent)