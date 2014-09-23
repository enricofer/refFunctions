# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_multiprint.ui'
#
# Created: Tue Jun 24 17:07:57 2014
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_multiPrint(object):
    def setupUi(self, multiPrint):
        multiPrint.setObjectName(_fromUtf8("multiPrint"))
        multiPrint.resize(239, 292)
        self.composerList = QtGui.QListWidget(multiPrint)
        self.composerList.setGeometry(QtCore.QRect(0, 30, 238, 201))
        self.composerList.setObjectName(_fromUtf8("composerList"))
        self.exportAsPdf = QtGui.QPushButton(multiPrint)
        self.exportAsPdf.setGeometry(QtCore.QRect(0, 265, 120, 23))
        self.exportAsPdf.setObjectName(_fromUtf8("exportAsPdf"))
        self.exportAsImg = QtGui.QPushButton(multiPrint)
        self.exportAsImg.setGeometry(QtCore.QRect(120, 265, 120, 23))
        self.exportAsImg.setObjectName(_fromUtf8("exportAsImg"))
        self.checkBox = QtGui.QCheckBox(multiPrint)
        self.checkBox.setGeometry(QtCore.QRect(0, 10, 151, 18))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.path = QtGui.QLineEdit(multiPrint)
        self.path.setGeometry(QtCore.QRect(0, 238, 151, 20))
        self.path.setObjectName(_fromUtf8("path"))
        self.browse = QtGui.QPushButton(multiPrint)
        self.browse.setGeometry(QtCore.QRect(160, 238, 75, 23))
        self.browse.setObjectName(_fromUtf8("browse"))

        self.retranslateUi(multiPrint)
        QtCore.QMetaObject.connectSlotsByName(multiPrint)

    def retranslateUi(self, multiPrint):
        multiPrint.setWindowTitle(_translate("multiPrint", "multiPrint", None))
        self.exportAsPdf.setText(_translate("multiPrint", "Export as PDFs", None))
        self.exportAsImg.setText(_translate("multiPrint", "Export as Imgs", None))
        self.checkBox.setText(_translate("multiPrint", "Select all", None))
        self.browse.setText(_translate("multiPrint", "Browse", None))

