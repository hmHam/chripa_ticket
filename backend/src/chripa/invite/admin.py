from django.contrib import admin
from chripa.invite.models import Invite, ParticipationLog
# Register your models here.
admin.site.register(Invite)
admin.site.register(ParticipationLog)
