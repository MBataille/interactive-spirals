# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'slice.ui'
##
## Created by: Qt User Interface Compiler version 6.2.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QSizePolicy, QWidget)

from pyqtgraph import PlotWidget

class Ui_Slice(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(600, 300)
        self.pwabs = PlotWidget(Form)
        self.pwabs.setObjectName(u"pwabs")
        self.pwabs.setGeometry(QRect(0, 0, 300, 300))
        self.pwang = PlotWidget(Form)
        self.pwang.setObjectName(u"pwang")
        self.pwang.setGeometry(QRect(300, 0, 300, 300))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

