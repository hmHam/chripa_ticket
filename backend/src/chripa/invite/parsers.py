import base64
import hashlib
import json
from Crypto.Cipher import AES
from django.conf import settings
from rest_framework.parsers import JSONParser
from rest_framework.serializers import ValidationError

# FIXME:
# 暗号化の第一の目的は、カメラのQRコードリーダーなどで中身が見えないようにすることである
# 第二の目的として、不正に何度もチケットQRコードの受領ログを送信し招待客数を誤魔化すことを防ぐことであるが
# これは今のところ実現されていないのでなにかしらの工夫が必要


class LogParser(JSONParser):
    def parse(self, stream, media_type=None, parser_context=None):
        data = super().parse(stream, media_type, parser_context)
        if 'info' not in data:
            raise ValidationError('送信データが不正です')
        data['info'] = self.decrypt_qrinfo(data['info'])
        print(data)
        return data

    @staticmethod
    def decrypt_qrinfo(b64encrypted_data):
        '''
        settingsのSECRET_KEYと初期化ベクトルIVを用いて暗号化されている
        チケット情報を復号する処理
        '''
        # 入力はb64でエンコードされているのでまず暗号化データにデコード
        encrypted_data = base64.b64decode(b64encrypted_data)
        cryptor = AES.new(
            hashlib.sha256(settings.SECRET_KEY.encode()).digest(),
            AES.MODE_CBC,
            hashlib.md5(settings.IV.encode()).digest()
        )
        b64data = cryptor.decrypt(encrypted_data)
        # 最後にjsonデータまで直す
        return json.loads(base64.b64decode(b64data))
