# -*- coding: utf-8 -*-
"""
/***************************************************************************
 multiPrintDialog
                                 A QGIS plugin
 print multiple print composer views
                             -------------------
        begin                : 2014-06-24
        copyright            : (C) 2014 by enrico ferreguti
        email                : enricofer@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os

from PyQt4 import QtGui, uic

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_multiprint.ui'))

class multiPrintDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(multiPrintDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

#from PyQt4 import QtCore, QtGui
#from ui_multiprint import Ui_multiPrint
# create the dialog for zoom to point

#class multiPrintDialog(QtGui.QDialog, Ui_multiPrint):
#class multiPrintDialog(QtGui.QDialog, Ui_multiPrint):
#    def __init__(self):
#        QtGui.QDialog.__init__(self)
#        # Set up the user interface from Designer.
#        # After setupUI you can access any designer object by doing
#        # self.<objectname>, and you can use autoconnect slots - see
#        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
#        # #widgets-and-dialogs-with-auto-connect
#        self.setupUi(self)
