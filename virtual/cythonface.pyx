import time
import numpy
cimport numpy
cimport cython
import cv2
ctypedef numpy.uint_t DTYPE_t
ctypedef numpy.uint8_t uint8
ctypedef numpy.int32_t int32
from PIL import Image,ImageColor

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)


def facedectmain(int32 [:, :] keypoints, uint8 [:, :,:] img1,str color ,  str partname):
    cdef int k = 6
    cdef int w,h,c,f,s
    w = img1.shape[0]
    h = img1.shape[1]
    c = img1.shape[2]
    f = 7
    s = 10
    cdef uint8 [:, :, :] mask,img2
    cdef uint8 R, G, B
    R,G,B = ImageColor.getcolor(color, "RGB")
    img2  = numpy.full((w,h,c) , [R,G,B],dtype=numpy.uint8)
    mask = numpy.zeros((w,h,c),dtype=numpy.uint8)
    mask = makepartmask(mask, keypoints, partname)
    mask = cv2.bitwise_and(numpy.uint8(mask), numpy.uint8(img2))
    mask = cv2.GaussianBlur(numpy.uint8(mask), (f, f), s)
    img1 = cv2.addWeighted(numpy.uint8(img1), 1, numpy.uint8(mask), 0.4, 0)
    return img1

def makepartmask(uint8 [:, :,:] mask,  int32 [:,:] keypoints, str partname):
  cdef list temp = []
  cdef str outer , inner , part
  cdef list chk = []
  cdef int index,x,y
  cdef list listloop

  if "Lip" in partname:
    listloop = ["upper"+partname , "lower"+partname]
  else:
    listloop = ["left"+partname , "right"+partname]

  for i in range(2):
    part = listloop[i]
    temp = []
    outer = part + "Outer"
    inner = part + "Inner"
    chk = []

    for index in annotations_dic[outer]:
      x =int(keypoints[index][0])
      y = int(keypoints[index][1])
      temp.append([x,y])
    chk.extend(temp)
    temp = []
    for index in annotations_dic[inner]:
      x =int(keypoints[index][0])
      y = int(keypoints[index][1])
      temp.append([x,y])
    temp.reverse()
    chk.extend(temp)
  mask = cv2.fillPoly(numpy.uint8(mask),numpy.int32([chk]), 255, lineType=cv2.LINE_AA)
  return mask



annotations_dic = \
  {"upperLipStickOuter": [61, 185, 40, 39, 37, 0, 267, 269, 270, 409, 291],
    "upperLipStickInner": [61,78, 191, 80, 81, 82, 13, 312, 311, 310, 415, 308,291],

   "lowerLipStickOuter": [61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291],
   "lowerLipStickInner": [61, 78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 291],

  "rightCreaseInner": [130,246, 161, 160, 159, 158, 157, 173],
  "rightCreaseOuter": [247, 30, 29, 27, 28, 56, 190],

  "rightCrease2Inner": [247, 30, 29, 27, 28, 56, 190,244],
  "rightCrease2Outer": [113, 225, 224, 223, 222, 221, 189,244],



  "rightLowerLashlineInner": [33, 7, 163, 144, 145, 153, 154, 155, 133],
  "rightLowerLashlineOuter": [130, 25, 110, 24, 23, 22, 26, 112, 243],

   "rightLowerLashline2Inner":  [130, 25, 110, 24, 23, 22, 26, 112, 243],
   "rightLowerLashline2Outer": [130, 117, 118, 119, 120],

   "rightLowerLashline3Inner": [35,31, 228, 229, 230, 231, 232],
  "rightLowerLashline3Outer": [ 35,111,117, 118, 119, 120],


  "rightEyeBrowsOuter": [70, 63, 105, 66, 107],
  "rightEyeBrowsInner": [53, 52, 65],



  "leftCreaseInner": [263,466, 388, 387, 386, 385, 384, 398,362],
  "leftCreaseOuter": [263,467, 260, 259, 257, 258, 286, 414,362],

  "leftCrease2Inner": [467, 260, 259, 257, 258, 286, 414],
  "leftCrease2Outer": [342, 445, 444, 443, 442, 441, 413],

"leftLowerLashlineInner": [263, 249, 390, 373, 374, 380, 381, 382, 362],
"leftLowerLashlineOuter": [359, 255, 339, 254, 253, 252, 256, 341, 463],

    "leftLowerLashline2Inner": [359, 255, 339, 254, 253, 252, 256, 341, 463],
    "leftLowerLashline2Outer": [446, 261, 448, 449, 450, 451, 452, 453, 464],

   "leftLowerLashline3Inner": [357, 451,450,449,448,261,265],
  "leftLowerLashline3Outer": [350, 349, 348, 347, 346, 340],


  "leftEyeBrowsOuter": [383, 300, 293, 334, 296, 336, 285, 417],
  "leftEyeBrowsInner": [265, 353, 276, 283, 282, 295],
  
  "midwayBetweenEyes": [168],

  "noseTip": [1],
  "noseBottom": [2],
  "noseRightCorner": [98],
  "noseLeftCorner": [327],

  "rightCheek": [50,101,36,206,207,187],
   #[117,118,101,36,205,187,137,234,117]
  "leftCheek": [330,266,426,427,411,280]
}
