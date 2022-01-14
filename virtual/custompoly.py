import numpy as np
import cv2
import time
import math


def real(mask, vertices):
    vertices = np.array(vertices, 'int32')
    mask = cv2.fillPoly(mask, [vertices], 255)
    return mask


def partition(newx, newy, low, high):
    i = (low - 1)  # index of smaller element
    pivot = newy[high]  # pivot

    for j in range(low, high):

        # If current element is smaller than or
        # equal to pivot
        if newy[j] <= pivot:
            # increment index of smaller element
            i = i + 1
            newy[i], newy[j] = newy[j], newy[i]
            newx[i], newx[j] = newx[j], newx[i]

    newy[i + 1], newy[high] = newy[high], newy[i + 1]
    newx[i + 1], newx[high] = newx[high], newx[i + 1]
    return (i + 1)


def quickSort(newx, newy, low, high):
    if len(newy) == 1:
        return newy
    if low < high:
        # pi is partitioning index, newy[p] is now
        # at right place
        pi = partition(newx, newy, low, high)

        # Separately sort elements before
        # partition and after partition
        quickSort(newx, newy, low, pi - 1)
        quickSort(newx, newy, pi + 1, high)


def horizontallines(x0, y0, x1, y1, mask):
    """Yield integer coordinates on the line from (x0, y0) to (x1, y1).
    Input coordinates should be integers.
    The result will contain both the start and the end point.
    """
    mask = cv2.circle(mask, (x1, y1), 1, (255, 255, 255), 1)
    # classifycolor(x1, y1, ffc_img)

    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0

    for x in range(dx + 1):
        px, py = x0 + x * xx + y * yx, y0 + x * xy + y * yy
        mask = cv2.circle(mask, (px, py), 1, (255, 255, 255), 1)
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy
    return mask


def verticallines(x0, y0, x1, y1, mask, newx, newy):
    dx = x1 - x0
    dy = y1 - y0

    xsign = 1 if dx > 0 else -1
    ysign = 1 if dy > 0 else -1

    dx = abs(dx)
    dy = abs(dy)

    if dx > dy:
        xx, xy, yx, yy = xsign, 0, 0, ysign
    else:
        dx, dy = dy, dx
        xx, xy, yx, yy = 0, ysign, xsign, 0

    D = 2 * dy - dx
    y = 0
    for x in range(dx + 1):
        px, py = x0 + x * xx + y * yx, y0 + x * xy + y * yy
        # yield px,py
        # mask = cv2.circle(mask, (px, py), 1, (255, 255, 255), 1)
        newx.append(px)
        newy.append(py)
        if D >= 0:
            y += 1
            D -= 2 * dx
        D += 2 * dy
    return mask, newx, newy


def customvertical(mask, vertices):
    pt0 = vertices[-1]
    newx = []
    newy = []
    for v in vertices:
        pt1 = v
        x1, y1 = pt0
        x2, y2 = pt1
        mask, newx, newy = verticallines(x1, y1, x2, y2, mask, newx, newy)
        pt0 = pt1

    return mask, newx, newy


def customhorizontal(mask, newx, newy):
    # print("count of newx ==", len(newx))
    # print("printing newx and  newy\n\n")
    quickSort(newx, newy, 0, len(newx) - 1)
    # for ii in range(len(newx)):
    #     print("(",newx[ii],",",newy[ii],"), ")
    j = 0
    for index, curr in enumerate(range(newy[0], newy[-1])):
        next = newy.index(curr + 1)
        minval = min(newx[j:next])
        maxval = max(newx[j:next])
        j = next
        mask = horizontallines(minval, curr, maxval, curr, mask)
    return mask


rfactor = 0;

def customfillpoly(mask,vertices):
    mask, newx, newy = customvertical(mask, vertices)
    mask = customhorizontal(mask, newx, newy)
    return  mask

# # import time
# mask1 = np.zeros((270, 270))
# mask2 = np.zeros((270, 270))
# mask3 = np.zeros((270,270))
# truex = np.load("truecoords.npz")["x"]
# truey = np.load("truecoords.npz")["y"]
# predx = np.load("predictedcoords.npz")["x"]
# predy = np.load("predictedcoords.npz")["y"]
# truex60 = np.load("truecoords60.npz")["x"]
# truey60 = np.load("truecoords60.npz")["y"]
#
# truevertices = [(int(x),int(y)) for x,y in zip(truex,truey)]
# mask1 = customfillpoly(mask1,truevertices)
# predvertices = [(int(x),int(y)) for x,y in zip(predx,predy)]
# mask2 = customfillpoly(mask2,predvertices)
# truevertices60 = [(int(x),int(y)) for x,y in zip(truex60,truey60)]
# mask3 = customfillpoly(mask3,truevertices60)
#
# cv2.imshow("mask1",mask1)
# cv2.imshow("mask2",mask2)
# cv2.imshow("mask3",mask3)
# cv2.imshow("diff",mask1-mask2)
#
#
# truecurvex  = []
# truecurvey = []
# for rows in range(270):
#     for cols in range(270):
#         if mask1[rows][cols]!=0:
#             truecurvex.append(cols)
#             truecurvey.append(rows)
#
#
# np.savez("truecurvex.npz",x = truecurvex)
# np.savez("truecurvey.npz",y = truecurvey)
#
#
#
# predcurvex = np.load("predcurvex.npz")["x"]
# predcurvey = np.load("predcurvey.npz")["y"]
#
# mask4 = np.zeros((270, 270))
# for i in range(len(predcurvex)):
#     mask4[int(predcurvey[i])][int(predcurvex[i])] = 1
# # truevertices = [(int(x),int(y)) for x,y in zip(predcurvex,predcurvey)]
# # mask3 = customfillpoly(mask3,truevertices)
#
# cv2.imshow("mask1",mask1)
# cv2.imshow("mask2",mask2)
# cv2.imshow("mask3",mask3)
# cv2.imshow("mask4",mask4)
# cv2.imshow("diff",mask1-mask3)
#
# # st2 = time.time()
# #
# # mask1 = real(realimg,vertices)
# # st3 = time.time()
# #
# #
# #
# # cv2.imshow("custom",mask)
# # cv2.imshow("real",mask1)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# # print("customtime ==",(st2-st1)*1000)
# # print("real===",(st3-st2)*1000)
# # # #
# # # plt.imshow(mask)
# #
#
