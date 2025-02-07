import cv2
import mediapipe as mp
import time

class FaceDetector():
    def __init__(self, minDetectionCon = 0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        # print(self.results)
        bboxes = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                    int(bboxC.width * iw), int(bboxC.height * ih)
                bboxes.append([id,bbox,detection.score ])
                if draw:
                    img = self.fancyDraw(img, bbox)
                    cv2.putText(img, f'{int(detection.score[0] * 100)}%',(bbox[0], bbox[1] -20), cv2.FONT_HERSHEY_PLAIN, 2, (211, 65, 89), 2)

        return img, bboxes
        
    def fancyDraw(self, img, bbox, l=30, t=5 , rt = 1):
        x, y, w, h = bbox
        x1, y1 = x+w , y+h

        cv2.rectangle(img, bbox, (255, 43, 123), rt)
        
        #Top left x,y
        cv2.line(img, (x,y), (x+l, y), (153,147,169), t)
        cv2.line(img, (x,y), (x, y+l), (153,147,169), t)
        #Top right x,y
        cv2.line(img, (x1,y), (x1-l, y), (153,147,169), t)
        cv2.line(img, (x1,y), (x1, y+l), (153,147,169), t)
        #Bottom left x,y
        cv2.line(img, (x,y1), (x+l, y1 ), (153,147,169), t)
        cv2.line(img, (x,y1), (x, y1-l), (153,147,169), t)
        #Bottom right x,y
        cv2.line(img, (x1,y1), (x1-l, y1), (153,147,169), t)
        cv2.line(img, (x1,y1), (x1, y1-l), (153,147,169), t)
        
        return img

def main():
    # cap = cv2.VideoCapture("./Face Detection/Videos/3.mp4")
    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceDetector()
    while True:
        success, img = cap.read()
        img, bboxes = detector.findFaces(img)
        print(bboxes)
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_PLAIN, 3, (23,45,34), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()