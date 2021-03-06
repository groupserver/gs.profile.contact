# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2016 Michael JasonSmith, OnlineGroups.net and Contributors.
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
from datetime import datetime, timedelta
from gs.database import getSession, getTable
from .audit import REQUEST_CONTACT, SUBSYSTEM


class RequestContactQuery(object):

    def __init__(self):
        self.auditEventTable = getTable('audit_event')

    def count_requests(self, uId):
        """ Get a count of the contact requests by this user in the last day.

:param str uId: The identifier of the person making the requests.
:returns: A count of the number of requests in the last 24 hours.
:rtype: int"""
        aet = self.auditEventTable
        statement = aet.select()
        statement.append_whereclause(aet.c.user_id == uId)
        td = datetime.now() - timedelta(days=1)
        statement.append_whereclause(aet.c.event_date >= td)
        statement.append_whereclause(aet.c.subsystem == SUBSYSTEM)
        statement.append_whereclause(aet.c.event_code == REQUEST_CONTACT)

        session = getSession()
        r = session.execute(statement)

        return r.rowcount
