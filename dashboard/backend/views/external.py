from structlog import get_logger

from django.views import View
from django.http import JsonResponse


LOGGER = get_logger(__name__)


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
    return JsonResponse({'success': 'OK!'})
