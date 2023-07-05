from typing import List
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from http.client import HTTPResponse
from django_backend.misc import printd
import json
import traceback

Scheme = 'http'
Host = '188.130.155.81:6379'
Address = f'{Scheme}://{Host}'


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

        content = response.read()
        if content is None: continue

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
    return result
