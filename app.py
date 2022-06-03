import urllib3
import time
import json
import cv2
import boto3
import os
from sendEmail import *

accessKey='' # ask admin to share access key
secretAccessKey='' # ask admin to share secret access
region='us-east-1'

door_api_request='https://api.thingspeak.com/channels/1757896/fields/1.json?api_key=MSFDSVRO49H43GOR&results=1'
door_push_request='https://api.thingspeak.com/update?api_key=6SSXG89IM231UG7X&field1=0'
person_push_request='https://api.thingspeak.com/update?api_key=6SSXG89IM231UG7X&field2='

family=os.listdir('family/')
dFlag=0

client=boto3.client('rekognition',aws_access_key_id=accessKey,aws_secret_access_key=secretAccessKey,region_name=region)

def takeSnapshot():
    print('Taking Photo')
    cam=cv2.VideoCapture(0)
    while True:
        res,frame=cam.read()
        if res:
            cv2.imshow('result',frame)
            cv2.imwrite('test.jpg',frame)
            # cv2.waitKey(1)
            break

    cv2.destroyAllWindows()
    cam.release()
    print('Snapshot Taken')

while True:
    http=urllib3.PoolManager()
    r=http.request('GET',door_api_request)
    r=(r.data.decode('utf-8'))
    r=json.loads(r)
    data=r['feeds'][0]['field1']
    print(data)
    if(data=='1'):
        # while True:
        #     r=http.request('GET',door_push_request)
        #     r=(r.data.decode('utf-8'))
        #     if(int(r)!=0):
        #         break
        print('Requesting Door')
        takeSnapshot()
        for i in family:
            imageSource=open('test.jpg','rb')
            imageTarget=open('family/'+i,'rb')
            response=client.compare_faces(SimilarityThreshold=70,SourceImage={'Bytes':imageSource.read()},TargetImage={'Bytes':imageTarget.read()})

            try:
                if response['FaceMatches']:
                    dFlag=1
                    result=i.split('.')[0]
                    print('Face Identified as ' + result)
                    send_email('otp.service@makeskilled.com','parvathanenimadhu@gmail.com','Face Identified as '+ result, 'Hi Hello, Alexa Bot Here','test.jpg')
                    while True:
                        r=http.request('GET',person_push_request+result)
                        r=(r.data.decode('utf-8'))
                        if(int(r)!=0):
                            break

                    break
            except:
                dFlag=0
        
        if(dFlag==0):
            print('Stranger Found')
            send_email('otp.service@makeskilled.com','parvathanenimadhu@gmail.com','Face Identified as Stranger', 'Hi Hello, Alexa Bot Here','test.jpg')
            while True:
                r=http.request('GET',person_push_request+'Stranger')
                r=(r.data.decode('utf-8'))
                if(int(r)!=0):
                    break
            

    time.sleep(0.05)