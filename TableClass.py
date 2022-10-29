from matplotlib import pyplot as plt

import numpy as np
from numpy.linalg import norm

import math as m

from shapely.geometry import Point

class Table :
    ## Define table dimensions in mm
    TABLE_TAG_SIZE = 100
    TABLE_TAG_LEFT_CORNER_X_OFFSET = 50
    TABLE_TAG_LEFT_CORNER_Y_OFFSET = 200 

    TABLE_LENGTH = 3000
    TABLE_WIDTH = 2000

    def __init__(self, arucoBoundaries):
        self.__arucoBoundaries = arucoBoundaries
        self.__scaleFactor = 0
        self.__center = []
        self.__origin = []
        self.__arucoBoundaries
        self.__areas = []

        self.__computeScaleFactor()
        self.__computeCenter()
        self.__computeOrigin()

    def __computeScaleFactor(self) :
        self.__scaleFactor = 1 * norm(self.__arucoBoundaries[0] - self.__arucoBoundaries[1], 2, axis = 0) / self.TABLE_TAG_SIZE

    def __computeCenter(self) :
        self.__center = self.__arucoBoundaries[0] + [-self.TABLE_TAG_LEFT_CORNER_X_OFFSET * self.__scaleFactor, 
                                                     self.TABLE_TAG_LEFT_CORNER_Y_OFFSET * self.__scaleFactor]
    
    def __computeOrigin(self) :
        self.__origin = self.__center + [self.TABLE_LENGTH * self.__scaleFactor / 2, self.TABLE_WIDTH * self.__scaleFactor /2]

    def drawArucoBoundaries(self, ax) :
        ax.add_patch(plt.Polygon(self.__arucoBoundaries, closed = True, fill = False, edgecolor = '#FF00FF', 
                                linewidth = 1, alpha = 0.5))

    def getOrigin(self) :
        return self.__origin

    def drawOrigin(self, ax) :
        self.__yAxisArrow = plt.arrow(self.__origin[0], self.__origin[1], 0, -100, color = '#FF00FF', alpha = 0.5, linewidth = 0.5, head_width = 20)
        ax.add_patch(self.__yAxisArrow)   
        self.__xAxisArrow = plt.arrow(self.__origin[0], self.__origin[1], -100, 0, color = '#FF00FF', alpha = 0.5, linewidth = 0.5, head_width = 20)
        ax.add_patch(self.__xAxisArrow)  

    def addArea(self, area) :
        self.__areas.append(area)

    def getArea(self) :
        return self.__areas

    def traceArea(self, ax) :
        for elt in self.__areas :
            elt.drawArea(ax)

    def getScaleFactor(self) :
        return self.__scaleFactor