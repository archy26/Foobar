# Foobar
hevo data assignment
# install pip
sudo apt-get install python3-pip
# install virtualenv
sudo pip3 install virtualenv
# create virtual env
virtualenv --python=python3.6 env
# activate virtualenv
source env/bin/activate
# install django
pip install Django
# go to the location where manage.py file is located and run this
python manage.py runserver

# How to get responses:
1) notification sender API ENDPOINT:- http://127.0.0.1:8000/send.notification?client_id=CX8291
body of this api :-
 [{
    "message":"Order updated",
    "type":"sms",
    "contact":"911"
},
{
    "message":"Order cancelled",
    "type":"email",
    "contact":"bazinga@bbt.com"
}
,
{
    "message":"Order cancelled",
    "type":"sms",
    "contact":"9000000002"
}
]
Response:
{
    "status": "success",
    "result": [
        {
            "message": "Order updated",
            "type": "sms",
            "time": "2021-08-22T18:15:19.878",
            "status": -1
        },
        {
            "message": "Order cancelled",
            "type": "email",
            "time": "2021-08-22T18:15:19.878",
            "status": 1
        },
        {
            "message": "Order cancelled",
            "type": "sms",
            "time": "2021-08-22T18:15:19.878",
            "status": 1
        }
    ]
}

2) statistics API ENDPOINT:- http://127.0.0.1:8000/statistics
Response:
{
    "status": "success",
    "result": {
        "CX8291": {
            "22-8-2021": {
                "total_message": 3,
                "failed_message": 1,
                "duplicate_message": 0
            }
        }
    }
}
3) Search API endpoint:- http://127.0.0.1:8000/search?client_id=CX8291&time=320&status=-1
   time params should be in seconds
   status of messages: 0 means duplicate message
                       1 means message delivered
                      -1 means message not delivered

Response:
{
"success": "search returned",
"result": [
    {
        "contact": "911",
        "message": "Order updated",
        "type": "sms",
        "status": -1
    }
]
}



   

