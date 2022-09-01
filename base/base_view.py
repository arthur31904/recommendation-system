# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import copy
import datetime
# from ..lib.i18n import LocalizerFactory

class BaseView(object):
    FormFactory = None

    def __init__(self, request, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self.request = request
        # self.localizer_factory = LocalizerFactory()
        # self.localizer = self.localizer_factory(request)
        # if self.FormFactory:
        #     self.form_factory = self.FormFactory(self.localizer)

        self.logger.info('[%s] %s - %s', self.request.method,
                         self.request.path_url, self.request.real_ip)

        self.request_params = self.request.params
        self.session = self.request.db_session
        self.settings = self.request.registry.settings

        self.request.response.headerlist.extend(
            (
                (str('Access-Control-Allow-Origin'), str('*')),
            )
        )
        self.request.response.charset = str('utf8')
        #
        # self.account_id = self.request.account_id if hasattr(self.request, 'account_id') else None
        # self.member_id = self.request.member_id if hasattr(self.request, 'member_id') else None

