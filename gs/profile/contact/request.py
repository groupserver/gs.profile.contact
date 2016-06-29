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
from __future__ import absolute_import, unicode_literals, print_function
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
# from zope.security.interfaces import Unauthorized
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.core import to_unicode_or_bust
from gs.profile.base import ProfileForm
from gs.profile.email.base.emailuser import EmailUser
from .audit import (Auditer, REQUEST_CONTACT)
from .interfaces import IRequestContact
from .notify import RequestNotifier
from .queries import RequestContactQuery


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
    def requestCount(self):
        if self.loggedInUser.anonymous:
            # FIXME: Figure out why raising Unauthorized does not work.
            # m = 'You must be logged in to request contact with someone.'
            # raise Unauthorized(m)
            u = '/login.html?came_from={0}/request_contact.html'
            uri = u.format(self.userInfo.url)
            retval = self.request.RESPONSE.redirect(uri)
        else:
            retval = self.queries.count_contactRequests(self.loggedInUser.id)
        return retval

    @Lazy
    def loggedInEmailUser(self):
        retval = EmailUser(self.context, self.loggedInUser)
        return retval

    @Lazy
    def emailUser(self):
        retval = EmailUser(self.context, self.userInfo)
        return retval

    @form.action(label='Request', name='request', failure='handle_set_action_failure')
    def handle_set(self, action, data):
        if self.requestCount > self.request24hrlimit:
            self.status = ('The request for contact has not been sent because you '
                           'have exceeded your daily limit of contact requests.')
        else:
            self.auditer = Auditer(self.userInfo, self.loggedInUser, self.siteInfo)
            message = to_unicode_or_bust(data.get('message', ''))
            self.auditer.info(REQUEST_CONTACT, message)
            self.request_contact(message)
            s = 'Your request has been sent to {0}.'
            self.status = s.format(self.userInfo.name)

        assert self.status

    def handle_set_action_failure(self, action, data, errors):
        if len(errors) == 1:
            self.status = '<p>There is an error:</p>'
        else:
            self.status = '<p>There are errors:</p>'

    def request_contact(self, userMessage):
        notifier = RequestNotifier(self.context, self.request)
        addr = self.loggedInEmailUser.preferred[0]
        notifier.notify(self.userInfo, self.loggedInUser, addr, userMessage)
