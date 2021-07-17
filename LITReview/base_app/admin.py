from django.contrib import admin
from django.contrib.auth.models import User
from . import models as mod

admin.site.register(mod.Ticket)
admin.site.register(mod.Review)
admin.site.register(mod.UserFollows)
