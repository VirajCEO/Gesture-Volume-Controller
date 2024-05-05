import cv2
import time
import modulegesture as  mgt
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import sys
###################################
wcam, hcam = 640, 480 

cap = cv2.VideoCapture(0)
cap.set(3, wcam)
cap.set(4, hcam)
ptime = 0
dectector = mgt.handdetecter(detectionCon=1)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))

volrange = volume.GetVolumeRange()

minvol = volrange[0]
maxvol = volrange[1]



def main():
  while True:
    success, img = cap.read()
    img  = dectector.FindHands(img)
    lmList = dectector.findPosition(img, draw=False)
    lmList2 = dectector.findPosition2(img,draw=False)
    
    if len(lmList) != 0:
    


     x1, y1 =lmList[4][1], lmList[4][2]
     x2, y2 =lmList[8][1], lmList[8][2]
     

    

     cv2.circle(img, (x1,y1), 5, (0,0,0),cv2.FILLED)
     cv2.circle(img, (x2,y2), 5, (0,0,0),cv2.FILLED)
     cv2.line(img, (x1,y1), (x2,y2),(0,0,0), 3 ) 
    
    
     
     length = math.hypot(x2 - x1, y2 - y1)
     
    

  
     vol = np.interp(length,[20,200], [minvol,maxvol])
     volume.SetMasterVolumeLevel(vol, None)


    if len(lmList2) != 0:

     x4, y4 =lmList2[4][1], lmList2[4][2]
     x3, y3 =lmList2[20][1], lmList2[20][2]
     length2 = math.hypot(x3 - x4, y3 - y4)   
     cv2.circle(img, (x4,y4), 5, (0,0,0),cv2.FILLED)
     cv2.circle(img, (x3,y3), 5, (0,0,0),cv2.FILLED)
     cv2.line(img, (x4,y4), (x3,y3),(0,0,0), 3 )  

     if length2 < 20:
        sys.exit()
      


    cv2.imshow("img", img)
    cv2.waitKey(1)
if __name__ == "__main__":
     main()
 
