from asyncio.windows_events import NULL
from matplotlib import pyplot as plt, scale

import numpy as np
from numpy.linalg import norm

import math as m

from shapely.geometry import Point


class Hex :
    ## Define constants
    RED_TAG_ID      = 47
    GREEN_TAG_ID    = 13
    BLUE_TAG_ID     = 36
    BACK_TAG_ID     = 17
    HEX_SIZE        = 150   #In mm
    HEX_TAG_SIZE    = 50    #In mm

    def __init__(self, arucoBoundaries, id): 
        self.__arucoBoundaries = arucoBoundaries
        self.__id = id

        self.__centerpx       = []
        self.__angle          = 0
        self.__sizeInPixels   = 0
        self.__scaleFactor    = 0
        self.__boundaries     = []
        self.__color          = ''
        self.__points         = 0 

        self.__computeColor()
        self.__computeCenter()
        self.__computeAngle()
        self.__computeScaleFactor()
        self.__computeSizeInPixels()
        self.__computeBoundaries()
    
    def __computeCenter(self) :
        self.__centerpx = np.mean(self.__arucoBoundaries, axis = 0)
        

    def __computeAngle(self)  :
        self.vectLength = norm(self.__arucoBoundaries[1] - self.__arucoBoundaries[2], axis=0)
        self.vectProjX  = abs(self.__arucoBoundaries[1, 1] - self.__arucoBoundaries[2, 1])
        self.__angle = (np.arccos(self.vectProjX/self.vectLength)) % m.pi/6

    def __computeScaleFactor(self) :
        self.__scaleFactor = norm(self.__arucoBoundaries[0] - self.__arucoBoundaries[1], 2, axis = 0) / self.HEX_TAG_SIZE

    def __computeSizeInPixels(self) :
         self.__sizeInPixels = self.HEX_SIZE * self.__scaleFactor / 2

    def __computeBoundaries(self) :
        for i in range(0, 7) :
            self.__boundaries.append([self.__centerpx[0] + self.__sizeInPixels * m.cos(self.__angle + i * m.pi/3),
                                    self.__centerpx[1] - self.__sizeInPixels * m.sin(self.__angle + i * m.pi/3)])

    def __computeColor(self) :
        if self.__id == self.RED_TAG_ID :
            self.__color = '#A81800'
        elif self.__id == self.GREEN_TAG_ID :
            self.__color = '#3EB73C'
        elif self.__id == self.BLUE_TAG_ID :
            self.__color = '#1784FF'
        elif self.__id == self.BACK_TAG_ID :
            self.__color = '#BF6A33'
        else :
            self.__color = '#BFBFBF'

    def __isInArea(self, table) :
        for area in table.getArea() :
            if Point(self.__centerpx[0], self.__centerpx[1]).within(area.getPoly()) :
                return area
        return NULL

    def computePoint(self, table) :
        ans = self.__isInArea(table)
        if  ans != NULL :
            self.__points = ans.getPoints()
            if self.__color == ans.getColor() :
                self.__points += 1

    def getCenterCoord(self,table, inMillimiters = True) :
        if inMillimiters :
            return (table.getOrigin() - self.__centerpx) / table.getScaleFactor()
        else :
            return self.__centerpx


    def drawCenter(self) :
        plt.scatter(self.__centerpx[0], self.__centerpx[1], s = 5, color = self.__color, marker = 's', linewidth = 0.5)

    def drawBoundaries(self, ax) :
        ax.add_patch(plt.Polygon(self.__boundaries, closed = True, fill = True, facecolor = self.__color, edgecolor = '#000000', 
                                linewidth = 0.5, alpha = 0.5))


    def drawArucoBoundaries(self, ax) :
        ax.add_patch(plt.Polygon(self.__arucoBoundaries, closed = True, fill = False, edgecolor = '#00FFFF', 
                                linewidth = 1, alpha = 0.5))

    def displayProperties(self, table) :
        center = self.getCenterCoord(table)
        plt.text(self.__centerpx[0], self.__centerpx[1], 'Center : ({}, {})\nAngle : {}\nColor : {}\nPoints : {}'
        .format(np.trunc(center[0]), np.trunc(center[1]), "{:.1f}".format(m.degrees(self.__angle)%180), self.__color, self.__points)
        , color = '#000000', size = 5)

    def displayAll(self, ax, table) :
        self.drawCenter()
        self.drawBoundaries(ax)
        self.drawArucoBoundaries(ax)
        self.displayProperties(table)