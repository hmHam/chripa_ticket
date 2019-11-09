from django.conf import settings

class ChripaDecoder:
  '''
  フロントエンドからログに送信してきたデータをsettingsのsecret_keyで復号する
  (
    qrcodeを読み取った際に意味のあるデータが見れないようにすることで
    認証情報を含んだデータはログインしていなくてもログを溜めれるようにする。
    （共通鍵暗号方式)
  )
  '''
  def __init__(self, request):
    self.get_reseponse = get_reseponse

  def __call__(self, request):
    pass