from typing import List
from urllib import request
from django_backend.misc import printd
import json
import traceback

Scheme = 'http'
Host = '95.217.166.108:6379'
Address = f'{Scheme}://{Host}'


def get(querytype: str, sites: List[str], query: str) -> List[dict]:
    result = []
    for site in sites:
        url = f'{Address}/get_{site}?{querytype}={query}'
        response = request.urlopen(url)

        printd(f'Data responded with {response.status_code} status code')
        if response.status_code != 200: continue

        content = response.content
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
