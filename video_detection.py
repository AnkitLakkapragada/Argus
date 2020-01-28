import numpy as np
import cv2
import imutils
import datetime
import socket
import geocoder
import smtplib 

from firebase import firebase
from ip2geotools.databases.noncommercial import DbIpCity
from twilio.rest import Client
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
firebase = firebase.FirebaseApplication('https://dvhacks-9ace0.firebaseio.com/')
client = Client("ACeab21caad55e235109cf7af1ff3df91d", "d219fc693f6526e4a09665b970c8e8dc")
client.messages.create(to="+14084294052", 
                       from_="15005550006", 
                       body="Hello from Python!")
gun_cascade = cv2.CascadeClassifier('cascade.xml')
camera = cv2.VideoCapture('data/gun4_2.mp4')
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)

firebase.post('', {'IP': IPAddr})
#response = DbIpCity.get(IPAddr, api_key='free')
firebase.post('', {'Lat': 37.7749})
firebase.post('', {'Lon': -122.4194})
#g = gecoder.ip('me')
#print(g.latlng)
print(IPAddr);

# initialize the first frame in the video stream
firstFrame = None

# loop over the frames of the video

gun_exist = False

while True:
    (grabbed, frame) = camera.read()

    # if the frame could not be grabbed, then we have reached the end of the video
    if not grabbed:
        break

    # resize the frame, convert it to grayscale, and blur it
    frame = imutils.resize(frame, width=500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    
    gun = gun_cascade.detectMultiScale(gray, 1.3, 5, minSize = (100, 100))
    
    if len(gun) > 0:
        gun_exist = True
        
    for (x,y,w,h) in gun:
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]    

    # if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue
    
    # draw the text and timestamp on the frame
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)

    # show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
    
    key = cv2.waitKey(1) & 0xFF

email = "john.sabantha@gmail.com"
pas = "iamjohnsabantha"

sms_gateway = '4083685638@txt.att.net'
# The server we use to send emails in our case it will be gmail but every email provider has a different smtp 
# and port is also provided by the email provider.
smtp = "smtp.gmail.com" 
port = 587
# This will start our email server
server = smtplib.SMTP(smtp,port)
# Starting the server
server.starttls()
# Now we need to login
server.login(email,pas)

# Now we use the MIME module to structure our message.
msg = MIMEMultipart()
msg['From'] = email
msg['To'] = sms_gateway
# Make sure you add a new line in the subject
msg['Subject'] = "Gun Detected Near You"
# Make sure you also add new lines to your body
body = "Please go to a safe and secure location and follow this feed as well as current news for more updates"
# and then attach that body furthermore you can also send html content.
msg.attach(MIMEText(body, 'plain'))

sms = msg.as_string()

server.sendmail(email,sms_gateway,sms)

# lastly quit the server
server.quit()

if gun_exist:
    print("guns detected")
else:
    print("guns NOT detected")

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()






