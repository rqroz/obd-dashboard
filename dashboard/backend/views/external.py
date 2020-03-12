from structlog import get_logger

from django.views import View
from django.http import HttpResponse
from backend.models.users import PQP
from django.views.decorators.csrf import csrf_exempt


LOGGER = get_logger(__name__)


@csrf_exempt
def external_input(request):
    LOGGER.info(
        'Request received on /external',
        headers=request.headers,
        body=request.body,
        scheme=request.scheme,
        path_info=request.path_info,
        method=request.method,
        encoding=request.encoding,
        content_type=request.content_type,
        params=request.content_params,
        get_data=request.GET,
        post_data=request.POST,
        files=request.FILES,
        cookies=request.COOKIES,
    )
    pqp = PQP(
        headers=request.headers,
        body=request.body,
        method=request.method,
        content_type=request.content_type,
        params=request.content_params,
        get_data=request.GET,
        post_data=request.POST,
        cookies=request.COOKIES,
    )
    pqp.save()
    return HttpResponse('OK!')
