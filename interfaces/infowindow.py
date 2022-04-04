# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'infowindow.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QSizePolicy, QWidget)

from pyqtgraph import ImageView

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(800, 500)
        self.im_abs = ImageView(Form)
        self.im_abs.setObjectName(u"im_abs")
        self.im_abs.setGeometry(QRect(0, 0, 400, 400))
        self.im_ang = ImageView(Form)
        self.im_ang.setObjectName(u"im_ang")
        self.im_ang.setGeometry(QRect(400, 0, 400, 400))
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 410, 791, 61))

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Info", None))
        self.label.setText(QCoreApplication.translate("Form", u"Params.", None))
    # retranslateUi

