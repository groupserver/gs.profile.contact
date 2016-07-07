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
from gs.profile.contact.notifications import (RequestContact, RequestContactText)


class TestRequestContact(TestCase):
    'Checking the ``RequestContact`` class'

    @staticmethod
    def u(name, url):
        retval = MagicMock()
        retval.name = name
        retval.url = url
        return retval

    @patch.object(RequestContact, 'set_skin')
    @patch.object(RequestContact, 'siteInfo', new_callable=PropertyMock)
    def test_get_support_email(self, m_siteInfo, m_set_skin):
        si = m_siteInfo()
        si.url = 'https://example.com'
        si.get_support_email.return_value = 'support@example.com'
        rc = RequestContact(MagicMock(), MagicMock())
        user = self.u('User', '/p/user')
        req = self.u('Requesting User', '/p/request')
        r = rc.get_support_email(user, req)

        self.assertEqual('mailto:', r[:7])
        self.assertNotIn(' ', r)
        self.assertIn('https%3A//example.com/p/user', r)
        self.assertIn('https%3A//example.com/p/request', r)


class TestRequestContactText(TestCase):

    long = ('On Ethel the Frog tonight we look at violence: the violence of British '
            'Gangland. Last Tuesday a reign of terror was ended when the notorious '
            'Piranha Brothers, Dug and Dinsdale ― after one the of most '
            'extraordinary trials in British legal history ― were sentenced to 400 '
            'years imprisonment for crimes of violence.')
    short = 'Tonight on Ethel the Frog we look at violence\u2026'

    @patch.object(RequestContact, 'set_skin')
    def test_format_message(self, m_set_skin):
        'Short lines should come back unchanged'
        rc = RequestContactText(MagicMock(), MagicMock())
        r = rc.format_message(self.short)

        self.assertEqual(self.short, r)

    @patch.object(RequestContact, 'set_skin')
    def test_format_message_indent(self, m_set_skin):
        rc = RequestContactText(MagicMock(), MagicMock())
        r = rc.format_message(self.short, indent='    ')

        self.assertEqual('    ' + self.short, r)

    @patch.object(RequestContact, 'set_skin')
    def test_format_message_wrap(self, m_set_skin):
        rc = RequestContactText(MagicMock(), MagicMock())
        r = rc.format_message(self.long)
        for i, line in enumerate(r.split('\n')):
            self.assertGreaterEqual(70, len(line),
                                    'Line {0} too long: {1}'.format(i, len(line)))
