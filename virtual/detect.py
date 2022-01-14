import base64
from io import BytesIO
import numpy as np
import cv2
# import dlib
import imutils
import numpy as np
from PIL import Image,ImageColor
from imutils import face_utils
from .annotations import  *
import sys
import logging
# sys.path.insert(0, "C:\\Users\\cheru\\Desktop\\maybelline\\virtual")
# import cython
# from .cythonface import *
import os

center_coordinates = (120, 50)
radius = 100
color = (255, 255, 255)
thickness = 50



def base64_decode(data):
    format, imgstr = data.split(';base64,')
    return base64.b64decode(imgstr)


def base64_encode(data):
    if data:
        return 'data:image/png;base64,'+ data.decode('utf-8')



def applyfilteronimage(image,keypoints,opacity,color,width,height,partsdic):
    nparr = np.fromstring(base64_decode(image), np.uint8)
    img1 = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img1  = cv2.cvtColor(img1,cv2.COLOR_RGB2BGR)
    keys= list(partsdic.keys())
    values = list(partsdic.values())
    # mask = np.zeros((int(height/2),int(width/2),3) ,dtype = np.uint8)
    mask = np.zeros((height,width,3) ,dtype = np.uint8)
    for i,value in enumerate(values):
        if value != "none":
            R,G,B = ImageColor.getcolor(value, "RGB")
            mask  = makepartmask(mask,keypoints ,keys[i])
            # img2  = np.full((int(height/2),int(width/2),3), (R,G,B) , dtype= np.uint8)
            img2  = np.full((height,width,3), (R,G,B) , dtype= np.uint8)
            mask = cv2.bitwise_and(mask, img2)

    mask = cv2.GaussianBlur(mask, (7, 7), 10)
     #       img1 = cv2.addWeighted(img1, 1, blurred_img, 0.4, 0)

            # img1[mask!=0] = img2[mask!=0]*0.3+0.7*img1[mask!=0]
            # alpha = 0.8
            # img1[mask != 0] = img2[mask != 0] * (1-alpha) + alpha * img1[mask != 0]
    #img1 = cv2.flip(img1,1)
    # mask = cv2.flip(mask,1)
    # mask = cv2.resize(mask,(width,height))
    # logging.info("image shaep == "  + str(img1.shape) +"mask sahpe == "+ str(mask.shape))
    img1 = cv2.addWeighted(img1, 1, mask, opacity/100, 0)
    # img1 = cv2.flip(img1,1)
    buffer = BytesIO()
    # img = Image.fromarray(mask)
    img = Image.fromarray(img1)

    # img = img.convert("rgb")
    img.save(buffer, format="jpeg")
    encoded_string = base64.b64encode(buffer.getvalue())
    return base64_encode(encoded_string)

def applyfilter(keypoints):
    mask = np.zeros((400,400))
    mask  = makepartmask(mask,keypoints ,"lipsUpperOuter")
    mask  = makepartmask(mask,keypoints ,"lipsLowerOuter")
    buffer = BytesIO()
    img = Image.fromarray(mask)
    img = img.convert("L")
    img.save(buffer, format="jpeg")
    encoded_string = base64.b64encode(buffer.getvalue())
    return base64_encode(encoded_string)
