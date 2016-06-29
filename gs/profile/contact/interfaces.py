# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright © 2013, 2016 E-Democracy.org and Contributors.
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
from zope.interface.interface import Interface
from zope.schema import TextLine


class IRequestContact(Interface):
    message = TextLine(
        title='Message',
        description='A message that will appear in the email to the person.'
                    ' It should be brief, as only 160 characters are allowed.',
        max_length=160,
        required=False)
