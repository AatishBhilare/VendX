from django.contrib import admin

# Register your models here.
from vmmanager.models import VmItem, Transaction

admin.site.register(VmItem)
admin.site.register(Transaction)