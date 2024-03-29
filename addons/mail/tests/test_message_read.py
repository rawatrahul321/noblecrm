# -*- coding: utf-8 -*-
# Part of NobleCRM. See LICENSE file for full copyright and licensing details.

from noblecrm.addons.mail.tests.common import TestMail
from noblecrm.tools import mute_logger


class TestMessageRead(TestMail):

    @mute_logger('noblecrm.addons.mail.models.mail_mail')
    def setUp(self):
        super(TestMessageRead, self).setUp()
        self.user_employee.write({'notification_type': 'inbox'})
        self.group_pigs.message_subscribe_users([self.user_employee.id])
        self.msg_0 = self.group_pigs.message_post(body='0', subtype='mt_comment')
        self.msg_1 = self.group_pigs.message_post(body='1', subtype='mt_comment')
        self.msg_2 = self.group_pigs.message_post(body='2', subtype='mt_comment')
        self.msg_3 = self.group_pigs.message_post(body='1-1', subtype='mt_comment', parent_id=self.msg_1.id)
        self.msg_4 = self.group_pigs.message_post(body='2-1', subtype='mt_comment', parent_id=self.msg_2.id)
        self.msg_5 = self.group_pigs.message_post(body='1-2', subtype='mt_comment', parent_id=self.msg_1.id)
        self.msg_6 = self.group_pigs.message_post(body='2-2', subtype='mt_comment', parent_id=self.msg_2.id)
        self.msg_7 = self.group_pigs.message_post(body='1-1-1', subtype='mt_comment', parent_id=self.msg_1.id)
        self.msg_8 = self.group_pigs.message_post(body='2-1-1', subtype='mt_comment', parent_id=self.msg_2.id)
        self.msg_9 = self.group_pigs.message_post(body='1-1-1', subtype='mt_comment', parent_id=self.msg_1.id)
        self.msg_10 = self.group_pigs.message_post(body='2-1-1', subtype='mt_comment', parent_id=self.msg_2.id)
        self.msg_ids = [self.msg_10.id, self.msg_9.id, self.msg_8.id, self.msg_7.id, self.msg_6.id, self.msg_5.id, self.msg_4.id, self.msg_3.id, self.msg_2.id, self.msg_1.id, self.msg_0.id]
        self.ordered_msg_ids = [self.msg_10.id, self.msg_8.id, self.msg_6.id, self.msg_4.id, self.msg_2.id, self.msg_9.id, self.msg_7.id, self.msg_5.id, self.msg_3.id, self.msg_1.id, self.msg_0.id]

    # TODO: test message_fetch
    # TODO: test message_(un)read
