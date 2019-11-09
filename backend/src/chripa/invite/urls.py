from django.urls import path
from rest_framework import routers
from chripa.invite.views import (
    InviteViewSet,
    ParticipationLogViewSet,
)
router = routers.SimpleRouter()
router.register('invites', InviteViewSet)
router.register('participations', ParticipationLogViewSet)
