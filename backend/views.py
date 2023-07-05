from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, FileResponse
from django.contrib.sessions.backends.base import SessionBase
from django_backend.misc import printd
from . import csvMaker
import io
import json


def process_query(request: HttpRequest):
    session: SessionBase = request.session
    printd(f'\nSession {session.session_key}')
    printd(f'''Remote IP: {request.META['REMOTE_ADDR']}''')
    if request.method == 'GET':
        printd(request.GET)
        # parse GET data
        # for each site selected
        # send to data
        # wait response
        # append to overall result
        # TEST
        with open('backend/sample.json', 'r', encoding = 'utf-8') as f:
            data = json.load(f)
        # ENDTEST
        printd(f'Type of data is {type(data).__name__}')
        printd(f'Type of data[0] is {type(data[0]).__name__}')
        session['data'] = data
        return HttpResponse(json.dumps(data), content_type = 'application/json')

    printd(f'Invalid \'{request.method}\' request is received')
    return HttpResponseBadRequest()


def csv_request(request: HttpRequest):
    session: SessionBase = request.session
    printd(f'\nSession {session.session_key}')
    if request.method == 'GET':
        # csv_str = csvMaker.make(session['data'])
        # TEST
        with open('backend/sample.json', 'r', encoding = 'utf-8') as f:
            csv_str = f.read()
        # ENDTEST
        return FileResponse(io.BytesIO(csv_str.encode()), as_attachment = True, filename = csvMaker.Filename)

    printd(f'Invalid \'{request.method}\' request is received')
    return HttpResponseBadRequest()
