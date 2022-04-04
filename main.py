from inspect import Parameter
from re import S
from PySide6 import QtWidgets, QtCore
from pyqtgraph.GraphicsScene import mouseEvents

from interfaces.mainwindow import Ui_MainWindow
from interfaces.infowindow import Ui_Form
from interfaces.slice import Ui_Slice
from qt_material import apply_stylesheet

import numpy as np

from functools import partial
import pyqtgraph as pg
from pyqtgraph.parametertree import Parameter, ParameterTree
import pyqtgraph.opengl as gl
import pandas as pd
import random
import time
import sys

FILES = {0.4: 's0.4.dat', 0.35: 's0.35.dat'}
SIGMA = 0.40
DATADIR = '/home/martin/Fisica/chimera/'
LOCALDIR = '/home/martin/Fisica/pyqt-course/interactive-spirals/'

HORIZONTAL = 'horizontal'
VERTICAL = 'vertical'

class DataReader:
    def __init__(self, sigma=0.4):
        self.sigma = sigma
        self.df = None

    def loadData(self):
        filename = LOCALDIR + 'data/' + FILES[self.sigma]
        self.df = pd.read_csv(filename)
        self.df['vxs'] *= -1

        self.N_curves = np.max(self.df['curve']) + 1

    def getAlphas(self, k=None):
        if self.df is None:
            self.loadData()
        if k is not None: 
            nk = self.getCurveN(k)

            # print('\n\n\n', k, '\n\n\n')

            return nk['alphas']
        return self.df['alphas']

    def getVxs(self, k=None):
        if self.df is None:
            self.loadData()
        if k is not None: 
            nk = self.getCurveN(k)

            # print('\n\n\n', k, '\n\n\n')

            return nk['vxs']
        return self.df['vxs']

    def getRs(self, k=None):
        if self.df is None:
            self.loadData()
        if k is not None: 
            return self.getCurveN(k)['Rs']
        return self.df['Rs']

    def getPaths(self, k=None):
        if self.df is None:
            self.loadData()
        if k is not None: 
            return self.getCurveN(k)['paths']
        return self.df['paths']

    def getClosest(self, alpha, vx):
        try:
            rel_dist = ((self.df['alphas'] / alpha - 1) ) ** 2 \
                        + ((self.df['vxs'] / vx - 1)) ** 2
        except ZeroDivisionError:
            return None

        self.closest = self.df.loc[np.argmin(rel_dist)]

        return {'alpha': self.closest['alphas'], 'vx': self.closest['vxs'], 
                'R': self.closest['Rs'], 'path': self.closest['paths']}

    def getCurveN(self, k):
        if k >= self.N_curves:
            return None

        return self.df.loc[self.df['curve'] == k]


    def getState(self, init=False):
        if init:
            path = self.df['paths'][0]
        else:
            path = self.closest['paths']

        path = DATADIR + path

        X = np.load(path)['X1']

        # assuming N = 128, symmetric
        N = 128
        z = X[:int(N*N/2)] + 1j * X[int(N*N/2):-2]
        z = z.reshape(int(N/2), N)
        z = np.concatenate((z, z[::-1, :]), axis=0)

        return z.T

class InfoWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.z = None
        self.sliceWindow = None

    def setSliceWindow(self, sliceWindow):
        self.sliceWindow = sliceWindow

    def showImage(self, z):

        for im in (self.im_abs, self.im_ang):
            im.show()
            im.ui.histogram.hide()
            im.ui.roiBtn.hide()
            im.ui.menuBtn.hide()

        self.cm_abs = pg.colormap.get('viridis', source='matplotlib')
        self.im_abs.setColorMap(self.cm_abs)
        #self.bar_abs = pg.ColorBarItem(cmap=self.cm_abs)
        #self.bar_abs.setImageItem(self.im_abs)
    
        self.im_ang.setColorMap(pg.colormap.get('hsv', source='matplotlib'))

        self.vb_abs = self.im_abs.getView()
        self.vb_ang = self.im_ang.getView()

        self.orientation = HORIZONTAL
        angle = self.orientationToAngle(self.orientation)
        self.il_abs = pg.InfiniteLine(pos = 64,angle=angle, movable=True, pen='k')
        self.il_ang = pg.InfiniteLine(pos = 64,angle=angle, movable=True, pen='k')

        self.il_abs.sigDragged.connect(self.updateAbsLine)
        self.il_ang.sigDragged.connect(self.updateAngLine)

        self.il_abs.sigClicked.connect(self.lineClicked)
        self.il_ang.sigClicked.connect(self.lineClicked)

        self.vb_abs.addItem(self.il_abs)
        self.vb_ang.addItem(self.il_ang)

        self.updateImage(z)

    def orientationToAngle(self, orientation):
        return 0 if orientation == HORIZONTAL else 90

    def angleToOrientation(self, angle):
        return HORIZONTAL if angle == 0 else VERTICAL

    def lineClicked(self):
        currentAngle = self.orientationToAngle(self.orientation)
        currentPos = self.il_abs.value()

        newAngle = 90 - currentAngle


        self.il_abs.setAngle(newAngle)
        self.il_ang.setAngle(newAngle)

        self.il_abs.setValue(currentPos) #somehow this is needed?
        self.il_ang.setValue(currentPos)

        self.orientation = self.angleToOrientation(newAngle)
        self.updateAngLine()
        self.updateAbsLine()

        print(self.il_abs.value())


    def updateLine(self):
        pos = self.il_abs.value()
        if self.sliceWindow is not None:
            self.sliceWindow.updateSlice(pos, self.orientation)

    def updateAngLine(self):
        self.il_abs.setValue(self.il_ang.value())
        self.updateLine()

    def updateAbsLine(self):
        self.il_ang.setValue(self.il_abs.value())
        self.updateLine()

    def updateImage(self, z):
        self.z = z
        self.im_abs.setImage(np.abs(self.z), levels=(0, 1))
        self.im_ang.setImage(np.angle(self.z), levels=(-np.pi, np.pi))


        #self.label.setText()

    def getMinMax(self):
        if self.z is not None:
            absz = np.abs(self.z)
            return absz.min(), absz.max()
        return -1, -1

    def updatePos(self, closest):
        min, max = self.getMinMax()
        txt = f'alpha = {closest["alpha"]}, vx = {closest["vx"]}\nmin = {min}, max = {max}'
        self.label.setText(txt)

class SliceWindow(QtWidgets.QWidget, Ui_Slice):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        
        self.orientation = HORIZONTAL
        self.pos = 0 # it will be changed to N/2 in showPlot

    def extract_absang(self, z):
        if self.pos < 0 or self.pos >= self.N: return None, None
        if self.orientation == HORIZONTAL:
            return np.abs(z[:, self.pos]), np.angle(z[:, self.pos])
        elif self.orientation == VERTICAL:
            return np.abs(z[self.pos, :]), np.angle(z[self.pos, :])

    def showPlot(self, z):

        #self.pwabs.show()
        #self.pwang.show()

        self.pwabs.setBackground('w')
        self.pwang.setBackground('w')

        self.N = z.shape[0]
        self.z = z
        self.pos = self.N // 2 # by default in the middle

        self.xs = np.linspace(-np.pi, np.pi, self.N)
        self.pen = pg.mkPen('b', width=3)
        
        absz, ang = self.extract_absang(z)
        
        self.abs_line = self.pwabs.plot(self.xs, absz, pen=self.pen)
        self.ang_line = self.pwang.plot(self.xs, ang, pen=self.pen)

    def updatePlot(self, z):
        self.z = z
        absz, ang = self.extract_absang(z)
        if absz is not None:
            self.abs_line.setData(self.xs, absz)
            self.ang_line.setData(self.xs, ang)

    def updateSlice(self, pos, orientation):
        self.orientation = orientation
        self.pos = int(round(pos))
        self.updatePlot(self.z)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.infowindow = InfoWindow()
        self.slicewindow = SliceWindow()
        self.infowindow.setSliceWindow(self.slicewindow)
        self.data = DataReader(sigma=SIGMA)

        self.showInfoWindow()
        self.showSliceWindow()

        self.loadData()

        # init image
        z = self.data.getState(init=True)
        self.infowindow.showImage(z)
        self.slicewindow.showPlot(z)

        self.drawPlot()


    def drawPlot(self):
        self.lines = []
        self.pw.setBackground('w')
        for i in range(self.data.N_curves):
            alphas = self.data.getAlphas(i).to_numpy()
            vxs = self.data.getVxs(i).to_numpy()
            line = self.pw.plot(alphas, vxs, pen=pg.mkPen('b', width=3))
            self.lines.append(line)
        
        print('plot ok')
        self.closest_point = self.pw.plot([self.alphas[0]], [self.vxs[0]], symbol='o', symbolsize=2)

        self.plotItem = self.pw.getPlotItem()

        proxy = pg.SignalProxy(self.plotItem.scene().sigMouseMoved, rateLimit=60, slot=self.mouseMoved)
        
        labelstyle = {'color' : '#000', 'font-size': '20px'}
        self.pw.setLabel('left', 'Vy', **labelstyle)
        self.pw.setLabel('bottom', 'alpha', **labelstyle)

    def closeEvent(self, event):
        self.infowindow.close()
        self.slicewindow.close()
        return super().closeEvent(event)

    def loadData(self):
        self.data.loadData()
        
        self.alphas = self.data.getAlphas()
        self.vxs = self.data.getVxs()

    def mouseMoved(self, evt):
        pos = evt[0]

        pi = self.plotItem
        if pi.sceneBoundingRect().contains(pos):
            mousePoint = pi.vb.mapSceneToView(pos)
            self.x, self.y = mousePoint.x(), mousePoint.y()

            xRatio = pos.x() / self.x
            yRatio = pos.y() / self.y

            # get closest point to mouse pos
            self.closest = self.data.getClosest(self.x, self.y)

            # update closest point in the plot
            self.closest_point.setData([self.closest['alpha']], [self.closest['vx']])
            
            # Show params in info view
            self.infowindow.updatePos(self.closest)

            # Show state (abs and arg of z)
            z = self.data.getState()

            self.infowindow.updateImage(z)
            self.slicewindow.updatePlot(z)

    def showInfoWindow(self):
        self.infowindow.show()

    def showSliceWindow(self):
        self.slicewindow.show()

if __name__ == '__main__':
    app = QtWidgets.QApplication()
    window = MainWindow()
    # apply_stylesheet(app, theme='light_blue.xml')

    window.show()
    sys.exit(app.exec())