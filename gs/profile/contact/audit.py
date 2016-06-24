# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2016 OnlineGroups.net and Contributors.
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
from datetime import datetime
from logging import getLogger
from pytz import UTC
from zope.component.interfaces import IFactory
from zope.interface import implementer, implementedBy
from Products.GSAuditTrail import (IAuditEvent, BasicAuditEvent, AuditQuery, event_id_from_data)

SUBSYSTEM = 'groupserver.ProfileAudit'
UNKNOWN = 0
REQUEST_CONTACT = '5'
log = getLogger(SUBSYSTEM)


@implementer(IFactory)
class AuditEventFactory(object):
    title = 'Request contact audit-event factory'
    description = 'Creates a GroupServer audit event for profiles'

    def __call__(self, context, event_id, code, date, userInfo, instanceUserInfo, siteInfo,
                 groupInfo=None, instanceDatum='', supplementaryDatum='', subsystem=''):

        if (code == REQUEST_CONTACT):
            event = RequestContactEvent(context, event_id, date, userInfo, instanceUserInfo,
                                        siteInfo, instanceDatum, supplementaryDatum)
        else:
            event = BasicAuditEvent(context, event_id, UNKNOWN, date, userInfo, instanceUserInfo,
                                    siteInfo, None, instanceDatum, supplementaryDatum, SUBSYSTEM)
        assert event
        return event

    def getInterfaces(self):
        return implementedBy(BasicAuditEvent)


@implementer(IAuditEvent)
class RequestContactEvent(BasicAuditEvent):
    """ A user requests contact with another user."""
    def __init__(self, context, id, d, userInfo, instanceUserInfo,
                 siteInfo, instanceDatum, supplementaryDatum):
        super(RequestContactEvent, self).__init__(
            context, id, REQUEST_CONTACT, d, userInfo, instanceUserInfo,
            siteInfo, None, instanceDatum, supplementaryDatum, SUBSYSTEM)

    def __unicode__(self):
        m = u'{0} ({1}) requested contact with {2} ({3})'
        retval = m.format(self.userInfo.name, self.userInfo.id,
                          self.instanceUserInfo.name, self.instanceUserInfo.id)
        return retval

    @property
    def xhtml(self):
        return unicode(self)


class Auditer(object):
    def __init__(self, userInfo, loggedInUserInfo, siteInfo):
        # --=mpj17=-- This is not a bug: what the audit-trail considers the
        # "user" is the person that is logged in. The "instance user" is the
        # person that is being acted on.
        self.userInfo = loggedInUserInfo
        self.instanceUserInfo = userInfo
        self.siteInfo = siteInfo
        self.queries = AuditQuery()
        self.factory = AuditEventFactory()

    def info(self, code, instanceDatum='', supplementaryDatum=''):
        print('HERE')
        d = datetime.now(UTC)
        eventId = event_id_from_data(self.userInfo, self.instanceUserInfo, self.siteInfo, code,
                                     instanceDatum, supplementaryDatum)
        e = self.factory(self.userInfo.user, eventId, code, d, self.userInfo, self.instanceUserInfo,
                         self.siteInfo, None, instanceDatum, supplementaryDatum, SUBSYSTEM)
        self.queries.store(e)
        log.info(e)
