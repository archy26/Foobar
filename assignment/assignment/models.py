import json
from .sender import Sender
import datetime
#stats contains all client_ids and their metrics partitioned by date
#{client_id:{date:{metrices}}}
stats = {}
#details dict contains all the messages sent by client key is client_id
# and then inside client_id there is a dict with key contact_number 
# and value is a list of all the details
#{client_id:{contact:[]}}
details ={}

class NotificationService(object):
    def send_notification(data,client_id):
        data = json.loads(data)
        if client_id not in stats:
            stats[client_id]={}
        if client_id not in details:
            details[client_id]={}
        #print(details)
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
            #print(duplicacy_flag,send_again)
            if d['type'] == 'email':
                if duplicacy_flag:
                    if send_again:
                        d['status'] = Sender.sendmail(contact,message)
                        response.append(d)
                    else:
                        d['status'] = 0
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
                        d['status'] = 0
                        response.append(d)
                else:
                    d['status'] = Sender.sendsms(contact,message)
                    response.append(d)

            if date not in stats[client_id]:
               stats[client_id][date]={ 'total_message':0,'failed_message':0,'duplicate_message':0}

            if d['status'] == -1:
                stats[client_id][date]['failed_message']+=1
            if duplicacy_flag:
                stats[client_id][date]['duplicate_message']+=1
                continue
            
            if contact not in details[client_id]:
                details[client_id][contact]=[]
            d.pop('contact')
            details[client_id][contact].append(d)
            stats[client_id][date]['total_message']+=1

        return response
    
    def statistics():
        return stats    

    def check_duplicate(data,client_id):
        
        contact = data['contact']
        now_time = data['time']
        #print(details)
        if client_id in details and contact in details[client_id]:
            for d in details[client_id][contact]:
                message = d['message'].strip()
                if data['message'].strip() == message:
                    total_seconds = (now_time-d['time']).total_seconds()
                    print(total_seconds)
                    #checking for repeating messages within 5 min
                    if total_seconds>=300:
                        return True,True
                    else:
                        return True,False
        return False,True

    def search(client_id,time,status = None):
        if client_id not in details:
            return []
        data = details[client_id]
        now = datetime.datetime.now() 
        response = []
        if status:
            status = int(status)
        for key,value in data.items():
            for info in value:
                body={}
                if status:
                    if status==info['status']:
                        later = info['time']
                        diff = int((now-later).total_seconds())
                        if time!=0 and diff<= time:
                            body['contact']=key
                            body['message'] =info['message']
                            body['type']=info['type']
                            body['status'] = info['status']
                        else:
                            body['contact']=key
                            body['message'] =info['message']
                            body['type']=info['type']
                            body['status'] = info['status']

                elif time!=0:
                    later = info['time']
                    diff = int((now-later).total_seconds())
                    if diff<= time:
                        body['contact']=key
                        body['message'] =info['message']
                        body['type']=info['type']
                        body['status'] = info['status']
                
                if len(body)>=1:
                    response.append(body)


        return response
            





