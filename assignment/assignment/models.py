import json
from .sender import Sender
import datetime
stats = {}
details ={}

class NotificationService(object):
    def send_notification(data,client_id):
        data = json.loads(data)
        if client_id not in stats:
            stats[client_id]={}
            details[client_id]={}
        print(data)
        response = []
        for d in data:    
            message = d['message']    
            contact = d['contact']   
            time = datetime.datetime.now() 
            year = time.year
            date = time.day
            month = time.month
            date = str(date)+"-"+str(month)+"-"+str(year)
            d['time'] = time
            duplicacy_flag,send_again = NotificationService.check_duplicate(d,client_id)
            if d['type'] == 'email':
                if duplicacy_flag:
                    if send_again:
                        d['status'] = Sender.sendmail(contact,message)
                        response.append(d)
                else:
                    d['status'] = Sender.sendmail(contact,message)
                    response.append(d)
            
            if d['type'] == 'sms':
                if duplicacy_flag:
                    if send_again:
                        d['status'] = Sender.sendsms(contact,message)
                        response.append(d)
                else:
                    d['status'] = Sender.sendsms(contact,message)
                    response.append(d)

            if date not in stats[client_id]:
               stats[client_id][date]={ 'total_message':0,'failed_message':0,'duplicate_message':0}

            print(duplicacy_flag)
            if d['status'] == -1:
                stats[client_id][date]['failed_message']+=1
            if duplicacy_flag:
                stats[client_id][date]['duplicate_message']+=1
            
            if contact not in details:
                details[client_id]={contact:[]}
            d.pop('contact')
            details[client_id][contact].append(d)
            stats[client_id][date]['total_message']+=1

        return response
    
    def statistics():
        return stats    

    def check_duplicate(data,client_id):
        
        contact = data['contact']
        now_time = data['time']
        if client_id in details and contact in details[client_id]:
            print(details)
            for d in details[client_id][contact]:
                message = d['message'].strip()
                if data['message'].strip() == message:
                    total_seconds = (d['time']-now_time).total_seconds()
                    if total_seconds>=300:
                        return True,False
                    else:
                        return True,True
        return False,True

    def search(client_id,time,status = None):
        data = details[client_id]
        now = datetime.datetime.now() 
        response = []
        for key,value in data.items():
            for info in value:
                body={}
                if status and status!=info['status']:
                    later = info['time']
                    diff = int((later-now).total_seconds())
                    if time and diff<= time:
                        body['contact']=key
                        body['message'] =info['message']
                        body['type']=info['type']
                        body['status'] = info['status']
                    else:
                        body['contact']=key
                        body['message'] =info['message']
                        body['type']=info['type']
                        body['status'] = info['status']

                else:
                    later = info['time']
                    diff = int((later-now).total_seconds())
                    if diff<= time:
                        body['contact']=key
                        body['message'] =info['message']
                        body['type']=info['type']
                        body['status'] = info['status']
                
                if len(body)>=1:
                    response.append(body)

        return response
            





