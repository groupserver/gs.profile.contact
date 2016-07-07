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
from email.Header import Header
from gs.content.email.base import NotifierABC
from gs.core import curr_time
from gs.profile.notify.sender import (MessageSender, UTF8)


class RequestNotifier(NotifierABC):
    htmlTemplateName = 'gs-profile-contact.html'
    textTemplateName = 'gs-profile-contact.txt'

    def notify(self, userInfo, requestingUserInfo, email, message):
        subject = 'Contact requested'
        text = self.textTemplate(userInfo=userInfo, requestingUserInfo=requestingUserInfo,
                                 email=email, message=message)
        html = self.htmlTemplate(userInfo=userInfo, requestingUserInfo=requestingUserInfo,
                                 email=email, message=message)
        sender = AlternateReplyMessageSender(self.context, userInfo)
        sender.send_message(subject, text, html)
        self.reset_content_type()


class AlternateReplyMessageSender(MessageSender):
    '''A message sender where the From and Reply-to are different'''
    def set_headers(self, container, subject, fromAddress, toAddresses):
        '''Like ``super.set_headers``, but sets the reply-to'''
        container['Subject'] = str(Header(subject, UTF8))
        container['From'] = self.from_header_from_address(None)  # Support
        container['To'] = self.to_header_from_addresses(toAddresses)
        container['Reply-to'] = fromAddress
        container['Date'] = curr_time().strftime('%a, %d %b %Y %H:%M:%S %z')
        return container
