import json
from .sender import Sender
import datetime
stats = {}
details ={}

class NotificationService(object):
    def send_notification(data,client_id):
        data = json.loads(data)
        if client_id not in stats:
            stats[client_id]={'total_message':0,'failed_message':0,'duplicate_message':0}
            details[client_id]={}
        print(data)
        response = []
        for d in data:    
            message = d['message']    
            contact = d['contact']   
            time = datetime.datetime.now() 
            d['time'] = time
            if d['type'] == 'mail':
                d['status'] = Sender.sendmail(contact,message)
                response.append(d)
            
            if d['type'] == 'sms':
                d['status'] = Sender.sendsms(contact,message)
                response.append(d)           
            duplicacy_flag = NotificationService.check_duplicate(d)
            if d['status'] == -1:
                stats[client_id]['failed_message']+=1
            if duplicacy_flag:
                stats[client_id]['duplicate_message']+=1
            
            if contact not in details:
                details[client_id]={contact:[]}
            details[client_id][contact].append(d.pop('contact'))
            stats[client_id]['total_message']+=1

        return response
    
    def statistics(client_id):
        return stats.get(client_id,{})
    
    def check_duplicate(data):
        client_id = data['client_id']
        contact = data['contact']
        if client_id in details and contact in details[client_id]:
            for d in details[client_id]:
                message = d['message'].strip()
                if data['message'].strip() == message:
                    return True
        return False