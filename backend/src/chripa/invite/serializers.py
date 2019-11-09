import hashlib
import base64
import json
from io import BytesIO

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone
from Crypto.Cipher import AES
import qrcode

from chripa.invite.models import Invite, ParticipationLog


class ParticipationLogSerializer(ModelSerializer):
    info = serializers.JSONField(write_only=True, help_text='QRコード情報')

    class Meta:
        model = ParticipationLog
        fields = [
            'id',
            'invite',
            'info',
            'had_visited',
            'visited_time',
        ]
        read_only_fields = [
            'had_visited',
            'visited_time',
        ]

    def validate_info(self, value):
        if 'inviter' not in value or not isinstance(value['inviter'], int):
            raise ValidationError("QRコード情報が不正です")
        if not User.objects.filter(id=value['inviter']).exists():
            raise ValidationError("招待者が存在しません")
        return value

    def create(self, validated_data):
        # FIXME: これだと通信するたびに更新されてしまう。一度だけ訪問した際に
        validated_data.pop('info')
        validated_data['had_visited'] = True
        validated_data['visited_time'] = timezone.now()
        return super().create(validated_data)


class InviteSerializer(ModelSerializer):
    class Meta:
        model = Invite
        fields = [
            'inviter',
            'ticket_price',
            'guest_name',
        ]

    def create(self, validated_data):
        try:
            self.context['qrcode'] = self.create_code(validated_data)
        except Exception as e:
            raise ValidationError(e.__class__.__name__)
        return super().create(validated_data)

    def create_code(self, validated_data):
        '''
        QRコードを生成する
        '''
        data = self.data_encrypt({
            'inviter': validated_data['inviter'].id,
            'ticket_price': validated_data['ticket_price']
        })
        code = qrcode.make(data)
        # TODO:(検討)生成したQRコードの画像をmediaに保存した後基礎情報を保存
        output_stream = BytesIO()
        code.save(output_stream)
        output_stream.seek(0)
        return output_stream

    @staticmethod
    def data_encrypt(validated_data):
        '''
        QRコードの情報を暗号化する処理
        QRコードリーダで読んだ値を見てもわからないものにする
        '''
        data = json.dumps(validated_data).encode()
        b64data = base64.b64encode(data)
        while len(b64data) % 16 != 0:
            b64data += b'_'
        cryptor = AES.new(
            hashlib.sha256(settings.SECRET_KEY.encode()).digest(),
            AES.MODE_CBC,
            hashlib.md5(settings.IV.encode()).digest()
        )
        encrypted_data = cryptor.encrypt(b64data)
        return base64.b64encode(encrypted_data)

    def to_representation(self, obj):
        data = super().to_representation(obj)
        data['inviter'] = obj['inviter'].username if isinstance(
            obj, dict) else obj.inviter.username
        return data
