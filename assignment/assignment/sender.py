import re
import smtplib

HOST_EMAIL="architsharma846@gmail.com"
HOST_PASSWORD="8295156554"
class Sender(object):
    def sendmail(email,message):

        if Sender.email_validation(email):
            i=0
            while i<3:
                try:
                    server=smtplib.SMTP_SSL("smtp.gmail.com",465)
                    server.login(HOST_EMAIL,HOST_PASSWORD)
                    server.send_message(HOST_EMAIL,email,message)
                    server.quit()
                    return 1
                except:
                    if i==2:
                        return -1
                    pass
        else:
            return -1

    def sendsms(number,message):
        if Sender.number_validation(number):
            print(message)
            return 1
        else:
            return -1

    def email_validation(email):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(email):
            return True
        else:
            return False

    def number_validation(number):
        number = str(number)
        if len(number)==10 and (number[0]>='6' and number[0]<='9'):
            return True
        else:
            return False

        


