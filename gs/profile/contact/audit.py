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
from zope.component.interfaces import IFactory
from zope.interface import implementer
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent

SUBSYSTEM = 'groupserver.ProfileAudit'
REQUEST_CONTACT = '5'


@implementer(IFactory)
class ProfileAuditEventFactory(object):
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
            self, context, id, REQUEST_CONTACT, d, userInfo, instanceUserInfo,
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
    def __init__(self, user):
        self.user = user
        self.userInfo = createObject('groupserver.LoggedInUser', user)
        self.instanceUserInfo = IGSUserInfo(user)
        self.siteInfo = createObject('groupserver.SiteInfo', user)
        self.queries = AuditQuery()
        self.factory = AuditEventFactory()

    def info(self, code, instanceDatum='', supplementaryDatum=''):
        d = datetime.now(UTC)
        eventId = event_id_from_data(self.userInfo, self.instanceUserInfo, self.siteInfo, code,
                                     instanceDatum, supplementaryDatum)
        e = self.factory(self.user, eventId, code, d, self.userInfo, self.instanceUserInfo,
                         self.siteInfo, None, instanceDatum, supplementaryDatum, SUBSYSTEM)
        self.queries.store(e)
        log.info(e)

