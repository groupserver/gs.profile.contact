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


class RequestContactQuery(object):

    def __init__(self):
        self.auditEventTable = getTable('audit_event')
        self.now = datetime.now()  # FIXME?

    def count_contactRequests(self):
        """ Get a count of the contact requests by this user in the past
            24 hours."""
        if self.anonymous_viewing_page:
            # FIXME: Figure out why raising Unauthorized does not work.
            # m = 'You must be logged in to request contact with someone.'
            # raise Unauthorized(m)
            uri = '/login.html?came_from=%s/request_contact.html' % \
                self.userInfo.url
            return self.request.RESPONSE.redirect(uri)

        aet = self.auditEventTable
        statement = aet.select()
        au = self.request.AUTHENTICATED_USER
        authUser = self.context.site_root().acl_users.getUser(au.getId())
        authUserInfo = IGSUserInfo(authUser)
        statement.append_whereclause(aet.c.user_id == authUserInfo.id)
        td = self.now - timedelta(1)
        statement.append_whereclause(aet.c.event_date >= td)
        subsystem = 'groupserver.ProfileAudit'
        statement.append_whereclause(aet.c.subsystem == subsystem)
        statement.append_whereclause(aet.c.event_code == REQUEST_CONTACT)

        session = getSession()
        r = session.execute(statement)
        return r.rowcount

