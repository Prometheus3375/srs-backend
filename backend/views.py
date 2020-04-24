from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, FileResponse
from django.contrib.sessions.backends.base import SessionBase
from django_backend.misc import printd
from typing import List, Tuple, Union
from . import csvMaker, dataGetter
import io
import json


def _parsePQGET(get: dict) -> Union[Tuple[str, List[str], str], None]:
    printd(get)
    if not ('sites' in get and 'query' in get):
        return None

    query = get['query']
    if not isinstance(query, str):
        printd(f'ERROR: given query is not a string')
        return None
    query = query.lower()

    sites = get['sites']
    if isinstance(sites, str):
        sites = [sites.lower()]
    elif isinstance(sites, list):
        for i in range(len(sites)):
            site = sites[i]
            if not isinstance(site, str):
                printd(f'ERROR: object on position {i} is sites is not a sting')
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
    session: SessionBase = request.session
    printd(f'\nSession {session.session_key}')
    printd(f'''Remote IP: {request.META['REMOTE_ADDR']}''')
    if request.method == 'GET':
        # get = _parsePQGET(request.GET)
        # if get is None:
        #     return HttpResponseBadRequest()
        # TEST
        get = 'category', ['amazon'], 'iphone11'
        # ENDTEST
        result = dataGetter.get(*get)
        # TEST
        # with open('backend/sample.json', 'r', encoding = 'utf-8') as f:
        #     result = json.load(f)
        # ENDTEST
        printd(f'Type of data is {type(result).__name__}')
        printd(f'Type of data[0] is {type(result[0]).__name__}')
        session['data'] = result
        return HttpResponse(json.dumps(result), content_type='application/json')

    printd(f'Invalid \'{request.method}\' request is received')
    return HttpResponseBadRequest()


def csv_request(request: HttpRequest):
    session: SessionBase = request.session
    printd(f'\nSession {session.session_key}')
    if request.method == 'GET':
        csv_str = csvMaker.make(session.get('data', []))
        # TEST
        # with open('backend/sample.json', 'r', encoding = 'utf-8') as f:
        #     csv_str = f.read()
        # ENDTEST
        return FileResponse(io.BytesIO(csv_str.encode()), as_attachment=True, filename=csvMaker.Filename)

    printd(f'Invalid \'{request.method}\' request is received')
    return HttpResponseBadRequest()
