# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SettingsManagerDialog
                                 A QGIS plugin
 Settings Manager
                             -------------------
        begin                : 2014-03-05
        copyright            : (C) 2014 by Rémi Bovard
        email                : remi.bovard@nyon.ch
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

from PyQt4 import QtCore, QtGui
from ui_settingsmanager import Ui_SettingsManager

class SettingsManagerDialog(QtGui.QDialog, Ui_SettingsManager):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
