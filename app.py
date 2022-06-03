import urllib3
import time
import json
import cv2

door_api_request='https://api.thingspeak.com/channels/1757896/fields/1.json?api_key=MSFDSVRO49H43GOR&results=1'
door_push_request='https://api.thingspeak.com/update?api_key=6SSXG89IM231UG7X&field1=0'

def takeSnapshot():
    print('Taking Photo')
    cam=cv2.VideoCapture(0)
    while True:
        res,frame=cam.read()
        if res:
            cv2.imshow('result',frame)
            cv2.imwrite('test.jpg',frame)
            cv2.waitKey(4)
            break

    cv2.waitKey(1)
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
    if(int(data)==1):
        while True:
            r=http.request('GET',door_push_request)
            r=(r.data.decode('utf-8'))
            if(int(r)!=0):
                break
        print('Requesting Door')
        takeSnapshot()
            


    time.sleep(4)