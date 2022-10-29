## Lib
import cv2
import cv2.aruco as aruco

import imutils

import matplotlib as mpl
from matplotlib import pyplot as plt
mpl.rcParams['figure.dpi']= 500

import numpy as np
from numpy.linalg import norm

import math as m

from HexClass import Hex
from AreaClass import Area
from TableClass import Table

TABLE_TAG_ID    = 42
DATA_SET_LENGTH = 25

def findAruco(img, markerSize = 4, totalMarkers = 250) :
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    arucoRequest = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(arucoRequest)
    arucoParam = aruco.DetectorParameters_create()
    bboxes, ids, _ = aruco.detectMarkers(grayImg, arucoDict, parameters = arucoParam)
    return ids, bboxes


for imNumber in range(0, DATA_SET_LENGTH+1) :

    img = cv2.imread('Input/in{}.png'.format(imNumber))
    img = imutils.rotate(img, angle=180)
    ids, bBoxes = findAruco(img)
    
    hexCollection = []

    for i in range(0, len(ids)) :
        if ids[i] == TABLE_TAG_ID :
            table = Table(bBoxes[i][0])
        else :
            hexCollection.append(Hex(bBoxes[i][0], ids[i]))

    yWorkShed = Area(table, [[0, 1690], [0, 2000], [310, 2000]], '#FF00FF', 5)
    yRedCampsite = Area(table, [[0, 400], [0, 1000], [130, 1000], [130, 400]], '#A81800', 1)
    yGreenCampsite = Area(table, [[130, 400], [130, 1000], [260, 1000], [260, 400]], '#3EB73C', 1)
    yBlueCampsite = Area(table, [[260, 400], [260, 1000], [390, 1000], [390, 400]], '#1784FF', 1)


    table.addArea(yWorkShed)
    table.addArea(yRedCampsite)
    table.addArea(yGreenCampsite)
    table.addArea(yBlueCampsite)

    img2Display = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    fig = plt.imshow(img2Display)
    fig.axes.get_xaxis().set_visible(False)
    fig.axes.get_yaxis().set_visible(False)

    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    table.traceArea(ax)
    table.drawOrigin(ax)
    table.drawArucoBoundaries(ax)

    for elt in hexCollection :
        elt.computePoint(table)
        elt.displayAll(ax, table)

    plt.savefig('Output/out{}'.format(imNumber), bbox_inches = None, pad_inches = 0)
    plt.close()