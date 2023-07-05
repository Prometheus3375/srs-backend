import json
import re
import traceback
from http.client import HTTPResponse
from typing import List
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from django_backend.misc import printd
from .misc import replace

Scheme = 'http'
Host = '188.130.155.81:6379'
Address = f'{Scheme}://{Host}'
_re_spaces = re.compile(r'\s+')
_url_start = r'http'


def postprocess(itemlist: List[dict]):
    """Converts fields' values of each object to proper strings or lists of string"""
    for obj in itemlist:
        for key, value in obj.items():
            if value is None:
                value = ''
            elif isinstance(value, list):
                # Clean values inside the list
                vals = []
                only_urls = True
                for v in value:
                    v = replace(str(v), _re_spaces, ' ').strip()
                    if len(v) == 0: continue
                    vals.append(v)
                    only_urls = only_urls and v.startswith(_url_start)
                # Join values if they are not URLs. Do not join if list is empty
                value = vals if only_urls else '\n'.join(vals)
            else:
                value = replace(str(value), _re_spaces, ' ').strip()
            # Change key if it is not a string
            if not isinstance(key, str):
                del obj[key]
                key = str(key)
            obj[key] = value


def get(querytype: str, sites: List[str], query: str) -> List[dict]:
    result = []
    for site in sites:
        url = f'{Address}/get_{site}?{querytype}={query}'
        try:
            response: HTTPResponse = urlopen(url)
        except (HTTPError, URLError) as e:
            traces = '\n'.join(traceback.format_tb(e.__traceback__))
            printd(f'An error occurred: {e} {{\n{traces}}}')
            continue

        status = response.getcode()
        printd(f'Data responded with {status} status code')
        if status != 200: continue

        content = response.read().strip()
        # TEST
        with open(f'latest-response-from-{site}.json', 'w', encoding = 'utf-8') as f:
            s = content.decode('utf-8')
            f.write(s)
        # ENDTEST
        if len(content) == 0: continue

        try:
            data = json.loads(content)
        except json.JSONDecodeError as e:
            traces = '\n'.join(traceback.format_tb(e.__traceback__))
            printd(f'An error occurred: {e} {{\n{traces}}}')
            continue

        if isinstance(data, list):
            result += data
        elif isinstance(data, dict):
            result.append(data)
    postprocess(result)
    return result
