# coding: utf-8
from __future__ import unicode_literals

import json

from .common import InfoExtractor
from .aws import AWSIE
from ..compat import compat_HTTPError
from ..utils import (
    clean_html,
    ExtractorError,
)


class ShahidBaseIE(AWSIE):
    _AWS_PROXY_HOST = 'api2.shahid.net'
    _AWS_API_KEY = 'YOUR_AWS_API_KEY_HERE'
    _VALID_URL_BASE = r'https?://shahid\.mbc\.net/[a-z]{2}/'

    def _handle_error(self, e):
        fail_data = self._parse_json(
            e.cause.read().decode('utf-8'), None, fatal=False)
        if fail_data:
            faults = fail_data.get('faults', [])
            faults_message = ', '.join([clean_html(fault['userMessage']) for fault in faults if fault.get('userMessage')])
            if faults_message:
                raise ExtractorError(faults_message, expected=True)

    def _call_api(self, path, video_id, request=None):
        query = {}
        if request:
            query['request'] = json.dumps(request)
        try:
            return self._aws_execute_api({
                'uri': '/proxy/v2/' + path,
                'access_key': 'YOUR_AWS_ACCESS_KEY_HERE',
                'secret_key': 'YOUR_AWS_SECRET_KEY_HERE',
            }, video_id, query)
        except ExtractorError as e:
            if isinstance(e.cause, compat_HTTPError):
                self._handle_error(e)
            raise


class ShahidIE(ShahidBaseIE):
    _VALID_URL = r'https?://shahid\.mbc\.net/[a-z]{2}/watch/(?P<id>\d+)'
    _TEST = {
        'url': 'https://shahid.mbc.net/ar/watch/123456',
        'only_matching': True,
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        return self._call_api('media/' + video_id, video_id)


class ShahidShowIE(ShahidBaseIE):
    _VALID_URL = r'https?://shahid\.mbc\.net/[a-z]{2}/show/(?P<id>\d+)'
    _TEST = {
        'url': 'https://shahid.mbc.net/ar/show/123456',
        'only_matching': True,
    }

    def _real_extract(self, url):
        show_id = self._match_id(url)
        return self._call_api('show/' + show_id, show_id)
