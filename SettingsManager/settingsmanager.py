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

    GEODATA_PATH = u"\\\\jupiter\\VDN_Commun\\SITNyon\\Geodata"

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, "i18n", "settingsmanager_{}.qm" . format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > "4.3.3":
                QCoreApplication.installTranslator(self.translator)

        self.dlg = SettingsManagerDialog()

    def initGui(self):
        self.action = QAction(QIcon(":/plugins/settingsmanager/icon.png"), u"Settings Manager", self.iface.mainWindow())
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
            self.__setWmsConnections(settings)
            self.__setPluginsSettings(settings)

            self.iface.messageBar().pushMessage(u"Paramètres SITNyon installés, redémarrer QGIS pour terminer l'installation.", level = QgsMessageBar.INFO)

    def __setOptions(self, settings):

        # General
        settings.setValue("Qgis/showTips", False)

        # System
        settings.setValue("svg/searchPathsForSVG", os.path.join(self.GEODATA_PATH, u"Impression\\Symboles"))

        # Data sources
        settings.setValue("Qgis/nullValue", "")
        settings.setValue("Qgis/addPostgisDC", True)

        # Map tools
        settings.setValue("Map/identifyMode", 3)
        settings.setValue("Map/identifyAutoFeatureForm", True)
        settings.setValue("Map/scales", u"1:100000,1:50000,1:25000,1:10000,1:5000,1:2500,1:1000,1:500,1:250,1:100")

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
        settings.setValue("browser/favourites", [os.path.join(self.GEODATA_PATH, u"Donnees")])

        # Last paths
        settings.setValue("UI/lastProjectDir", os.path.join(self.GEODATA_PATH, u"Projets"))
        settings.setValue("UI/lastVectorFileFilterDir", os.path.join(self.GEODATA_PATH, u"Donnees"))
        settings.setValue("UI/lastRasterFileFilterDir", os.path.join(self.GEODATA_PATH, u"Donnees\\Orthophotos"))
        settings.setValue("Qgis/last_embedded_project_path", os.path.join(self.GEODATA_PATH, u"Projets"))

    def __setWmsConnections(self, settings):

        # ASIT VD
        settings.setValue("Qgis/connections-wms/ASIT VD/url", u"https://secure.asitvd.ch/proxy/ogc/asitvd-wms-fonds")
        settings.setValue("Qgis/connections-wms/ASIT VD/dpiMode", 7)
        settings.setValue("Qgis/connections-wms/ASIT VD/ignoreAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/ASIT VD/ignoreGetFeatureInfoURI", False)
        settings.setValue("Qgis/connections-wms/ASIT VD/ignoreGetMapURI", False)
        settings.setValue("Qgis/connections-wms/ASIT VD/invertAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/ASIT VD/smoothPixmapTransform", False)
        settings.setValue("Qgis/WMS/ASIT VD/username", u"vdn")

        # Vaud
        settings.setValue("Qgis/connections-wms/Vaud/url", u"https://secure.asitvd.ch/proxy/ogc/vd-wms")
        settings.setValue("Qgis/connections-wms/Vaud/dpiMode", 7)
        settings.setValue("Qgis/connections-wms/Vaud/ignoreAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/Vaud/ignoreGetFeatureInfoURI", False)
        settings.setValue("Qgis/connections-wms/Vaud/ignoreGetMapURI", False)
        settings.setValue("Qgis/connections-wms/Vaud/invertAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/Vaud/smoothPixmapTransform", False)

    def __setPluginsSettings(self, settings):

        # Check updates
        settings.setValue("Qgis/plugin-installer/checkOnStart", True)
        settings.setValue("Qgis/plugin-installer/checkOnStartInterval", 7)

        # Experimental plugins
        settings.setValue("Qgis/plugin-installer/allowExperimental", True) # Allows experimental plugins but doesn't check the checkbox...
