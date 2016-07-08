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
from mock import (MagicMock, patch)
from unittest import TestCase
from gs.profile.contact.notify import AlternateReplyMessageSender


class TestAlternateReplyMessageSender(TestCase):
    @patch.object(AlternateReplyMessageSender, 'from_header_from_address')
    @patch.object(AlternateReplyMessageSender, 'to_header_from_addresses')
    def test_set_headers(self, m_to, m_from):
        m_to.return_value = 'Person <a.person@example.com>'
        m_from.return_value = 'Support <support@groups.example.com>'

        ms = AlternateReplyMessageSender(MagicMock(), MagicMock())
        container = {}
        ms.set_headers(container, 'Test', 'other@example.com', 'mocked')

        m_to.assert_called_once_with('mocked')
        m_from.assert_called_once_with(None)  # Did we generate the Support address?
        self.assertEqual(m_to(), container['To'])
        self.assertEqual('other@example.com', container['Reply-to'])
        self.assertEqual(m_from(), container['From'])
