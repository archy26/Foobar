from django.http import JsonResponse,HttpResponse
from .models import NotificationService
from django.views.decorators.csrf import csrf_exempt
import copy

@csrf_exempt
def sendNotification(request):
    data = request.body.decode("utf-8")
    response = {"status":"success"}
    request_get = copy.copy(request.GET.dict())
    client_id = request_get.get('client_id',None)
    if not client_id:
        response['status'] ='failed'
        response['result'] = "Client Id Not Found"
        return JsonResponse(response)
    result = NotificationService.send_notification(data,client_id)
    response['result'] =result
    return JsonResponse(response)

def statistics(request):
    response = {"status":"success"}
    response['result'] = NotificationService.statistics()
    return JsonResponse(response)

def search(request):
    response = {"success": "search returned"}
    request_get = copy.copy(request.GET.dict())
    client_id = request_get.get('client_id',None)
    time = int(request_get.get('time',0))
    status = request_get.get('status',None)

    response['result'] = NotificationService.search(client_id,time,status)
    return JsonResponse(response)
    