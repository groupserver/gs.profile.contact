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
from textwrap import TextWrapper
from gs.content.email.base import SiteEmail, TextMixin
from gs.profile.base import ProfilePage


class RequestContact(SiteEmail, ProfilePage):
    'Request contact with another member'

    def get_support_email(self, userInfo, requestingUserInfo):
        m = '''Hello,

I recieved a Contact request from {request.name}
    {siteInfo.url}{request.url}
and...

--
About me:
  {user.name}
  {siteInfo.url}{user.url}'''
        msg = m.format(user=userInfo, request=requestingUserInfo, siteInfo=self.siteInfo)
        subject = 'Contact request'
        retval = self.mailto(self.siteInfo.get_support_email(), subject, msg)
        return retval


class RequestContactText(RequestContact, TextMixin):

    def __init__(self, context, request):
        super(RequestContactText, self).__init__(context, request)
        self.set_header('request-contact-txt')

    @staticmethod
    def format_message(m, indent=''):
        tw = TextWrapper(width=70, initial_indent=indent, subsequent_indent=indent)
        retval = tw.fill(m)
        return retval
