======================
``gs.profile.contact``
======================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Request contact with another member of a GroupSever group
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2016-06-20
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

Introduction
============

GroupServer is built around the principal of *lurk in peace:*
just reading messages (lurking) is a valid form of participation,
and group members should be left alone if they lurk. However,
there are times when it would be nice to contact a lurking group
member. This product supports this edge-case.

The page ``request_contact.html`` (in the context of a profile)
allows someone that is logged in to send a short message to
someone. Along with the message all the **contact details** for
the person **making** the request is sent. The person being
contacted then has a choice to respond, or to ignore the
request. The contact details of the recipient are always kept
confidential.

The HTML and plain-text form of the notifications themselves are
formatted by ``gs-profile-contact.html`` and
``gs-profile-contact.txt`` respectively (in the context of a
profile).

Resources
=========

- Code repository:
  https://github.com/groupserver/gs.profile.contact
- Questions and comments to
  http://groupserver.org/groups/development
- Translations:
  https://www.transifex.com/projects/p/gs-profile-contact
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17

..  LocalWords:  nz GSProfile TODO redirector LocalWords
