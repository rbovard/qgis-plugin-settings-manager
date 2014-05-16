# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SettingsManager
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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import resources_rc
from settingsmanagerdialog import SettingsManagerDialog
import os.path

class SettingsManager:

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'settingsmanager_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        self.dlg = SettingsManagerDialog()

    def initGui(self):
        self.action = QAction(
            QIcon(":/plugins/settingsmanager/icon.png"),
            u"Settings Manager", self.iface.mainWindow())

        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Settings Manager", self.action)

    def unload(self):
        self.iface.removePluginMenu(u"&Settings Manager", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        self.dlg.show()
        result = self.dlg.exec_()

        if result == 1:
            settings = QSettings()

            self.__setOptions(settings)
            self.__setToolbarsVisibility()
            self.__setPaths(settings)

            self.iface.messageBar().pushMessage(u"Paramètres SITNyon installés", level=QgsMessageBar.INFO, duration=3)

    def __setOptions(self, settings):

        # General
        settings.setValue("Qgis/showTips", False)

        # System
        settings.setValue("svg/searchPathsForSVG", u"\\\\jupiter\\VDN_Commun\\SITNyon\\Geodata\\Impression\\Symboles\\")

        # Data sources
        settings.setValue("Qgis/nullValue", "")
        settings.setValue("Qgis/addPostgisDC", True)

        # Map tools
        settings.setValue("Map/identifyAutoFeatureForm", True)

        # Composer
        settings.setValue("Composer/defaultFont", u"Gill Sans MT")

        # Digitizing
        settings.setValue("Qgis/digitizing/default_snap_mode", u"to vertex and segment")
        settings.setValue("Qgis/digitizing/default_snapping_tolerance", 5)

        # CRS
        settings.setValue("Projections/otfTransformAutoEnable", False)
        settings.setValue("Projections/otfTransformEnabled", False)
        settings.setValue("Projections/projectDefaultCrs", u"EPSG:21781")
        settings.setValue("Projections/layerDefaultCrs", u"EPSG:21781")

        # Network
        settings.setValue("proxy/proxyEnabled", True)
        settings.setValue("proxy/proxyHost", u"193.135.104.6")
        settings.setValue("proxy/proxyPort", 8080)
        settings.setValue("proxy/proxyType", u"HttpProxy")

    def __setToolbarsVisibility(self):

        # Visible
        self.iface.attributesToolBar().setVisible(True)
        self.iface.digitizeToolBar().setVisible(True)
        self.iface.fileToolBar().setVisible(True)
        self.iface.layerToolBar().setVisible(True)
        self.iface.mapNavToolToolBar().setVisible(True)

        # Hidden
        self.iface.advancedDigitizeToolBar().setVisible(False)
        self.iface.databaseToolBar().setVisible(False)
        self.iface.helpToolBar().setVisible(False)
        self.iface.pluginToolBar().setVisible(False)
        self.iface.rasterToolBar().setVisible(False)
        self.iface.vectorToolBar().setVisible(False)
        self.iface.webToolBar().setVisible(False)
        self.iface.mainWindow().findChild(QToolBar, "mLabelToolBar").setVisible(False)

    def __setPaths(self, settings):

        # Favourites
        settings.setValue("browser/favourites", [u"\\\\jupiter\\VDN_Commun\\SITNyon\\Geodata\\Donnees"])

        # Last paths
        settings.setValue("UI/lastProjectDir", u"\\\\jupiter\\VDN_Commun\\SITNyon\\Geodata\\Projets")
        settings.setValue("UI/lastVectorFileFilterDir", u"\\\\jupiter\\VDN_Commun\\SITNyon\\Geodata\\Donnees")
        settings.setValue("UI/lastRasterFileFilterDir", u"\\\\uranus\\SITNYON_GEODONNEES\\010_DONNEES_DE_REFERENCE\\012_ORTHOPHOTO")
        settings.setValue("Qgis/last_embedded_project_path", u"\\\\jupiter\\VDN_Commun\\SITNyon\\Geodata\\Projets")
