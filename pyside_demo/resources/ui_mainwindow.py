# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
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
from PySide6.QtWidgets import (QApplication, QMainWindow, QSizePolicy, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.sidebar_widget = QWidget(self.centralwidget)
        self.sidebar_widget.setObjectName(u"sidebar_widget")
        self.sidebar_widget.setGeometry(QRect(5, 60, 50, 535))
        self.sidebar_widget.setStyleSheet(u"QWidget{\n"
"	background-color: rgb(63, 63, 63);\n"
"}")
        self.drawer_widget = QWidget(self.centralwidget)
        self.drawer_widget.setObjectName(u"drawer_widget")
        self.drawer_widget.setGeometry(QRect(60, 60, 200, 535))
        self.drawer_widget.setStyleSheet(u"background-color: rgb(53, 53, 53);")
        self.header_widget = QWidget(self.centralwidget)
        self.header_widget.setObjectName(u"header_widget")
        self.header_widget.setGeometry(QRect(5, 5, 790, 50))
        self.header_widget.setStyleSheet(u"background-color: rgb(53, 53, 53);")
        self.main_screen_widget = QWidget(self.centralwidget)
        self.main_screen_widget.setObjectName(u"main_screen_widget")
        self.main_screen_widget.setGeometry(QRect(265, 60, 530, 535))
        self.main_screen_widget.setStyleSheet(u"background-color: rgb(53, 53, 53);")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
    # retranslateUi

