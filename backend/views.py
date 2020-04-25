import io
import json
from typing import List, Tuple, Union

from django.contrib.sessions.backends.base import SessionBase
from django.http import FileResponse, HttpRequest, HttpResponseBadRequest, JsonResponse

from django_backend.misc import printd
from . import csvMaker, dataGetter


def _parsePQBody(body_bytes: bytes) -> Union[Tuple[str, List[str], str], None]:
    printd(f'Bytes in the body: {body_bytes}')
    try:
        body = json.loads(body_bytes)
    except json.JSONDecodeError:
        return None

    if not (isinstance(body, dict) and 'sites' in body and 'query' in body):
        return None

    query = body['query']
    if not isinstance(query, str):
        printd(f'ERROR: given query is not a string')
        return None
    query = query.lower()

    sites = body['sites']
    if isinstance(sites, str):
        sites = [sites.lower()]
    elif isinstance(sites, list):
        for i in range(len(sites)):
            site = sites[i]
            if not isinstance(site, str):
                printd(f'ERROR: object on position {i} is sites is not a string')
                return None
            sites[i] = site.lower()
    else:
        printd(f'ERROR: given sites are not a list or a string')
        return None
    # For now only one site is expected
    if len(sites) != 1:
        printd(f'ERROR: for now only 1 site is allowed')
        return None

    site = sites[0]
    if site == 'amazon':
        querytype = 'category'
    elif site == 'airbnb':
        querytype = 'city'
    else:
        printd(f'ERROR: only amazon and airbnb sites are allowed')
        return None

    return querytype, sites, query


def process_query(request: HttpRequest):
    printd('\nRequest is sent to /api/process-query')
    session: SessionBase = request.session
    printd(f'Session {session.session_key}')
    if request.method == 'POST':
        body = _parsePQBody(request.body)
        if body is None:
            return HttpResponseBadRequest()
        # TEST
        # body = 'category', ['amazon'], 'iphone11'
        # body = 'city', ['airbnb'], 'kazan'
        # ENDTEST
        result = dataGetter.get(*body)
        # TEST
        # with open('backend/sample.json', 'r', encoding = 'utf-8') as f:
        #     result = json.load(f)
        # ENDTEST
        printd(f'Type of result is {type(result).__name__}')
        if len(result) > 0:
            printd(f'    type of result[0] is {type(result[0]).__name__}')
        else:
            printd(f'    result is empty')

        session['data'] = result
        session.modified = True  # to ensure that changes will be saved
        return JsonResponse(result, safe = False)

    printd(f'Invalid \'{request.method}\' request is received')
    return HttpResponseBadRequest()


def csv_request(request: HttpRequest):
    printd('\nRequest is sent to /api/make-csv')
    session: SessionBase = request.session
    printd(f'Session {session.session_key}')
    if request.method == 'GET':
        csv_str = csvMaker.make(session.get('data', []))
        return FileResponse(io.BytesIO(csv_str.encode()), as_attachment = True, filename = csvMaker.Filename)

    printd(f'Invalid \'{request.method}\' request is received')
    return HttpResponseBadRequest()
