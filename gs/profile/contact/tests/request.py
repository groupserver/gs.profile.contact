# -*- coding: utf-8 -*-
############################################################################
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
############################################################################
from __future__ import absolute_import, unicode_literals, print_function
from mock import (MagicMock, PropertyMock, patch)
from unittest import TestCase
from gs.profile.contact.request import (RequestContact)


class TestRequestContact(TestCase):

    @patch.object(RequestContact, 'requestCount', new_callable=PropertyMock)
    def test_handle_set_limit(self, m_requestCount):
        'Ensure we handle the request-limit being hit'
        m_requestCount.return_value = RequestContact.request24hrlimit + 1
        rc = RequestContact(MagicMock(), MagicMock())
        # Calling the handle_set method this way because how the zope.formlib.form.action
        # decorator works
        rc.handle_set.success_handler(rc, MagicMock(), MagicMock())

        self.assertEqual('request-quota-hit', rc.status)

    @patch.object(RequestContact, 'requestCount', new_callable=PropertyMock)
    @patch.object(RequestContact, 'userInfo', new_callable=PropertyMock)
    @patch.object(RequestContact, 'request_contact')
    @patch.object(RequestContact, 'audit')
    def test_handle_set(self, m_audit, m_request_contact, m_userInfo, m_requestCount):
        m_requestCount.return_value = 0
        rc = RequestContact(MagicMock(), MagicMock())
        m = 'Tonight on Ethel the Frog we look at violence\u2026'
        data = {'message': m, }
        rc.handle_set.success_handler(rc, MagicMock(), data)

        m_request_contact.assert_called_once_with(m)
        m_audit.assert_called_once_with(m)
        self.assertEqual('request-success', rc.status)
