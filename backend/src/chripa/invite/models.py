from django.db import models
from django.contrib.auth.models import User
from chripa.models import ModelBase


class Invite(ModelBase):
    class Meta:
        verbose_name = verbose_name_plural = '招待'
        ordering = ['-created']
    inviter = models.ForeignKey(
        User, verbose_name='招待者', on_delete=models.PROTECT)
    ticket_price = models.IntegerField(verbose_name='チケット値段')
    guest_name = models.CharField('ゲスト名', max_length=100)

    def __str__(self):
        return "{inviter}招待の{guest_name}さん(¥{price})".format(
            guest_name=self.guest_name,
            inviter=self.inviter.username,
            price=self.ticket_price
        )


class ParticipationLog(ModelBase):
    class Meta:
        verbose_name = verbose_name_plural = '参加確認ログ'
        ordering = ['-created']
    invite = models.ForeignKey(
        Invite, verbose_name='招待', on_delete=models.PROTECT)
    had_visited = models.BooleanField('来訪', default=False)
    visited_time = models.DateTimeField(verbose_name='来店時刻', null=True)
