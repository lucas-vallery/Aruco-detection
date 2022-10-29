## Librairies
import cv2
import cv2.aruco as aruco
from matplotlib import pyplot as plt

from HexClass import Hex
from AreaClass import Area

## Fonctions
def findAruco(img, markerSize = 4, totalMarkers = 250, drawTheMarkers = True) :
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    arucoRequest = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(arucoRequest)
    arucoParam = aruco.DetectorParameters_create()
    bboxes, ids, _ = aruco.detectMarkers(grayImg, arucoDict, parameters = arucoParam)
    #print(bboxes, ids)
    return ids, bboxes


## Processing
img=cv2.imread("RawData/TableWithElement1.png")

id, bbox = findAruco(img)

hexCollection = []

for i in range(0, len(id)):
    hexCollection.append(Hex(bbox[i][0], id[i]))


## Display

img2Display = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.imshow(img2Display)
ax = plt.gca()

for elt in hexCollection :
    elt.displayAll(ax)
    #print(elt.getCenterCoord())

plt.show()