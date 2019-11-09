from django.http import FileResponse
from rest_framework.renderers import AdminRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

from chripa.invite.models import Invite, ParticipationLog
from chripa.invite.serializers import InviteSerializer, ParticipationLogSerializer
from chripa.invite.parsers import LogParser


class InviteViewSet(ModelViewSet):
    serializer_class = InviteSerializer
    queryset = Invite.objects.all()
    renderer_classes = [AdminRenderer]
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return FileResponse(
            serializer.context['qrcode'],
            as_attachment=True,
            content_type='image/png',
            filename='{}({})招待.png'.format(
                serializer.instance.guest_name,
                serializer.instance.inviter.username
            )
        )


class ParticipationLogViewSet(ModelViewSet):
    queryset = ParticipationLog.objects.all()
    serializer_class = ParticipationLogSerializer
    parser_classes = [LogParser]
    http_method_names = ['get', 'post']
