from django.http import JsonResponse


def health_check(request):
    response_data = {
        "status_code": 200,
        "detail": "ok",
        "result": "working"
    }

    json_response = JsonResponse(response_data, json_dumps_params={'indent': 2})
    return json_response
