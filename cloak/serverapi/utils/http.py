"""
A simple HTTP wrapper that manages standard headers and error responses.

Most clients will want to include the 'auth' keyword argument with credentials.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import requests
from six.moves import xrange
from six.moves.urllib.parse import urljoin
from typing import Any  # noqa

from cloak.serverapi.errors import ServerApiError


session = requests.Session()


# This can be overridden for test environments.
base_url = 'https://www.getcloak.com/'


def get(path, api_version=None, **kwargs):
    # type: (str, str, **Any) -> requests.Response
    return _call('GET', path, api_version, **kwargs)


def post(path, api_version=None, **kwargs):
    # type: (str, str, **Any) -> requests.Response
    return _call('POST', path, api_version, **kwargs)


def _call(method, path, api_version=None, **kwargs):
    # type: (str, str, str, **Any) -> requests.Response
    url = urljoin(base_url, '/api/server/')
    url = urljoin(url, path)

    headers = kwargs.setdefault('headers', {})
    if api_version is not None:
        headers['X-Cloak-API-Version'] = api_version

    if method == 'GET':
        response = session.get(url, **kwargs)
    elif method == 'POST':
        response = session.post(url, **kwargs)
    else:
        raise NotImplementedError()

    if response.status_code not in xrange(200, 400):
        raise ServerApiError(response)

    return response
