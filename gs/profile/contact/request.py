# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2014, 2016 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
# from zope.security.interfaces import Unauthorized
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.core import to_unicode_or_bust
from gs.profile.base import ProfileForm
from gs.profile.email.base.emailuser import EmailUser
from .interfaces import IRequestContact
from .audit import REQUEST_CONTACT, Auditer


class RequestContact(ProfileForm):
    label = 'Request contact'
    pageTemplateFileName = 'browser/templates/request.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IRequestContact, render_context=False)
    request24hrlimit = 3  # --=mpj17=-- Considering more than three requests a day to be harassment

    def __init__(self, context, request):
        super(RequestContact, self).__init__(context, request)

    @Lazy
    def queries(self):
        retval = RequestContactQuery()
        return retval

    @Lazy
    def loggedInEmailUser(self):
        retval = EmailUser(self.context, self.loggedInUser)
        return retval

    @form.action(label='Request', name='request', failure='handle_set_action_failure')
    def handle_set(self, action, data):
        if self.queries.count_contactRequests() > self.request24hrlimit:
            self.status = ('The request for contact has not been sent because you '
                           'have exceeded your daily limit of contact requests.')
        else:
            self.auditer = ProfileAuditer(self.context)
            message = to_unicode_or_bust(data.get('message', ''))
            self.request_contact(message)
            s = 'The request for contact has been sent to {0}.'
            self.staus = s.format(self.userInfo.name)

        assert self.status

    def handle_set_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = '<p>There is an error:</p>'
        else:
            self.status = '<p>There are errors:</p>'

    def request_contact(self, userMessage):
        # TODO: This method.
        pass

