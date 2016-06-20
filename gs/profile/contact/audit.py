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
from zope.interface import implementer
from Products.GSAuditTrail import IAuditEvent, BasicAuditEvent

SUBSYSTEM = 'groupserver.ProfileAudit'
REQUEST_CONTACT = '5'


@implementer(IAuditEvent)
class RequestContactEvent(BasicAuditEvent):
    """ A user requests contact with another user."""
    def __init__(self, context, id, d, userInfo, instanceUserInfo,
                 siteInfo, instanceDatum,  supplementaryDatum):
        super(RequestContactEvent, self).__init__(
            self, context, id, REQUEST_CONTACT, d, userInfo, instanceUserInfo,
            siteInfo, None,  instanceDatum, supplementaryDatum, SUBSYSTEM)

    def __unicode__(self):
        m = u'{0} ({1}) requested contact with {2} ({3})'
        retval = m.format(self.userInfo.name, self.userInfo.id,
                          self.instanceUserInfo.name, self.instanceUserInfo.id)
        return retval

    @property
    def xhtml(self):
        return unicode(self)

