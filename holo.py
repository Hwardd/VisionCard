import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from PIL import ImageGrab
from globalData import *


#print(someCards)

def buildTemplateArray( ):
    "Build template array"
    newTemplate = []
    for card in someCards:
        newTemplate.append(cv.imread(card,0))
    return newTemplate

templateCards= buildTemplateArray()


while(1):
    img = ImageGrab.grab(bbox=(100,100,1200,900)) #bbox specifies specific region (bbox= x,y,width,height *starts top-left)
    img_np = np.array(img) #this is the array obtained from conversion
    img_gray = cv.cvtColor(img_np, cv.COLOR_BGR2GRAY)
    img_show = cv.cvtColor(img_np,cv.COLOR_BGR2RGB)
    
    for template in templateCards:
        w, h = template.shape[::-1]
        res = cv.matchTemplate(img_gray,template,cv.TM_CCOEFF_NORMED)
        threshold = 0.95
        loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            cv.rectangle(img_show, pt, (pt[0] + w, pt[1] + h), (0,255,0), 2)

    cv.imshow("test", img_show)
    k=cv.waitKey(100) & 0xFF 

    if k == ord('q'):
        break
cv.destroyAllWindows()
