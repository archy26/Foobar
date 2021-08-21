from django.http import JsonResponse,HttpResponse
from .models import NotificationService
from django.views.decorators.csrf import csrf_exempt
import copy
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def sendNotification(request):
    data = request.body.decode("utf-8")
    response = {"success":"message sent"}
    request_get = copy.copy(request.GET.dict())
    client_id = request_get.get('client_id',None)
    if not client_id:
        response['result'] = "Client Id "
        return JsonResponse(response)
    result = NotificationService.send_notification(data,client_id)
    response['result'] =result
    return JsonResponse(response)

def statistics(request):
    response = {"success": "stats returned"}
    request_get = copy.copy(request.GET.dict())
    client_id = request_get.get('client_id',None)
    response['result'] = NotificationService.statistics(client_id)
    return JsonResponse(response)

def search(request):
    response = {"success": "stats returned"}
    request_get = copy.copy(request.GET.dict())
    client_id = request_get.get('client_id',None)
    response = {"success": "stats returned"}
    return JsonResponse(response)
    