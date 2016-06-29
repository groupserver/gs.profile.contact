# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2016 Michael JasonSmith and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from __future__ import absolute_import, unicode_literals, print_function
from gs.content.email.base import NotifierABC


class RequestNotifier(NotifierABC):
    htmlTemplateName = 'gs-profile-contact.html'
    textTemplateName = 'gs-profile-contact.txt'

    def notify(self, userInfo, requestingUserInfo, email, message):
        subject = 'Contact requested'
        text = self.textTemplate(userInfo=userInfo, requestingUserInfo=requestingUserInfo,
                                 email=email, message=message)
        html = self.htmlTemplate(userInfo=userInfo, requestingUserInfo=requestingUserInfo,
                                 email=email, message=message)

        sender = MessageSender(self.context, userInfo)
        sender.send_message(subject, text, html)
        self.reset_content_type()

