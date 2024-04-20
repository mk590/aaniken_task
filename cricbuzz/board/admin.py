from django.contrib import admin
from .models import CustomUser,Player,Team,Match

admin.site.register([CustomUser,Player,Team,Match])