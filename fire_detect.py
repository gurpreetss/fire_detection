import pyshine
import cv2
import numpy as np
import time
from gpiozero import Buzzer

buzzer = Buzzer(17)

def play_sound():
    count = 3;
    while count>0:
        buzzer.on()
        time.sleep(0.5)
        buzzer.off()
        time.sleep(0.5)
        count = count -1

# define a video capture object
vid = cv2.VideoCapture(0)

# Fire detection parameters
isFire = False
threshold = 40000

start = None
black_color = (0, 0, 0)
red_color = (255, 0, 0)
text = "Fire Detected!!!"


frame_count = 0


while(True):
    frame_count = frame_count+1
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    if ret and (frame_count%10==0):
        blur = cv2.GaussianBlur(frame, (21,21), 0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        lower = np.array([1,30,169], dtype = "uint8")
        upper = np.array([36,255,255], dtype = "uint8")
        mask1 = cv2.inRange(hsv,lower,upper)
        lower = np.array([30,0,245], dtype = "uint8")
        upper = np.array([180,8,255], dtype = "uint8")
        mask2 = cv2.inRange(hsv,lower,upper)
        fmask = cv2.bitwise_or(mask1,mask2)
        firecount = cv2.countNonZero(fmask)
        print(firecount)
        output = cv2.bitwise_and(frame, frame, mask = fmask)
        isFire = firecount > threshold
        if isFire:
            output = pyshine.putBText(frame, text, text_offset_x=200, text_offset_y=50, \
                                  vspace=10, hspace=10, font_scale=1.0, background_RGB=red_color, text_RGB=black_color)
            cv2.imshow("Fire detector ", output)
            play_sound()
            cv2.waitKey()
            #time.sleep(5)
        else:
            cv2.imshow("Fire detector ", frame)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

