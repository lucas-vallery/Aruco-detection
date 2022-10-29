from matplotlib import pyplot as plt
from shapely.geometry import Polygon

class Area :
    def __init__(self, table, corners, color, points):
        self.__color = color
        self.__team = 0
        self.__corners = corners   #In mm
        self.__drawCorners = []
        self.__points = points

        self.__computePolyCorners(table)
        self.__poly = Polygon(self.__drawCorners)

    def __computePolyCorners(self, table) :
        self.__tableOrigin = table.getOrigin()
        self.__scaleFactor = table.getScaleFactor()

        for i in range(0, len(self.__corners)) :
            self.__temp = [self.__corners[i][0] * self.__scaleFactor, self.__corners[i][1] * self.__scaleFactor] 
            self.__drawCorners.append(self.__tableOrigin - self.__temp)
    
    def drawArea(self, ax) :
        ax.add_patch(plt.Polygon(self.__drawCorners, closed = True, fill = True, color = self.__color, 
                                linewidth = 1, alpha = 0.5))

    def getCorners(self) :
        return self.__corners

    def getPoly(self) :
        return self.__poly
    
    def getColor(self) :
        return self.__color
    
    def getPoints(self) :
        return self.__points