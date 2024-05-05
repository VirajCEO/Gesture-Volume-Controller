import cv2
import mediapipe as mp
import time
class handdetecter():
    
    def __init__(self, mode=False , maxHands=2, detectionCon=0.5, trackCon=0.5  ):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mphands = mp.solutions.hands
        self.hands = self.mphands.Hands(self.mode,self.maxHands,self.detectionCon,self.trackCon)
        self.mpdraw = mp.solutions.drawing_utils


    def FindHands(self, img ,draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
         for handLms in self.results.multi_hand_landmarks:
            if draw:
             self.mpdraw.draw_landmarks(img, handLms, self.mphands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img,handNo=0,draw=True):
     lmList = []
     if self.results.multi_hand_landmarks:
      myHand = self.results.multi_hand_landmarks[handNo]
      for id, lm in enumerate(myHand.landmark):
        # print(id, lm)
        h, w, c = img.shape
        
        cx, cy = int(lm.x * w), int(lm.y * h)

        lmList.append([id, cx, cy])
     
        if draw:
         cv2.circle(img, (cx,cy),5,(255,0,255),cv2.FILLED)
     return lmList

    def findPosition2(self,img,handNo=-1,draw=True):
     lmList2 = []
     if self.results.multi_hand_landmarks:
      myHand2 = self.results.multi_hand_landmarks[handNo]
      for id, lm in enumerate(myHand2.landmark):
        # print(id, lm)
        h2, w2, c = img.shape
        
        cx2, cy2 = int(lm.x * w2), int(lm.y * h2)

        lmList2.append([id, cx2, cy2])
     
        if draw:
         cv2.circle(img, (cx2,cy2),5,(255,0,255),cv2.FILLED)
     return lmList2
  


def main():
    pTime = 0
    cap = cv2.VideoCapture(0)
    detecter = handdetecter()
    while True:
        success, img = cap.read()
        img = detecter.FindHands(img)
        lmList = detecter.findPosition(img)
        lmList2 = detecter.findPosition2(img)
        if len(lmList2) != 0:
           print(lmList2[0])
    
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
    
        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
        (255, 0, 255), 3)
    
        cv2.imshow("Image", img)
        cv2.waitKey(1)

    
if __name__ == "__main__":
    main()
