from django.views import View
from django.http import JsonResponse


def external_input(request):
    from pprint import pprint
    print('------------------------- START ---------------------------')
    print('Headers:')
    pprint(request.headers)
    print('Body:')
    pprint(request.body)
    print(f'Scheme: {request.scheme}')
    print(f'Path Info: {request.path_info}')
    print(f'Method: {request.method}')
    print(f'Encoding: {request.encoding}')
    print(f'Content Type: {request.content_type}')
    print(f'Content Params: {request.content_params}')
    print(f'GET data: {request.GET}')
    print(f'POST data: {request.POST}')
    print(f'Files: {request.FILES}')
    print(f'Cookies: {request.COOKIES}')
    print('-------------------------- END ----------------------------')
    return JsonResponse({'success': 'OK!'})
