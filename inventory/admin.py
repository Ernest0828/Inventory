from django.contrib import admin
from .models import Items
import data_wizard

# Register your models here.
admin.site.register(Items)
data_wizard.register(Items)
