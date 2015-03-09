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

    GEODATA_PATH = u"\\\\orcus\\SITNyon\\Geodata"
    settings = QSettings()

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
            self.__setOptions()
            self.__setToolbarsVisibility()
            self.__setPaths()
            self.__setWmsConnections()
            self.__setPlugins()

            self.iface.messageBar().pushMessage(u"Installation", u"Paramètres SITNyon importés, redémarrer QGIS pour terminer l'installation.", level = QgsMessageBar.INFO)

    def __setOptions(self):

        # General
        self.settings.setValue("Qgis/showTips", False)

        # System
        self.settings.setValue("svg/searchPathsForSVG", os.path.join(self.GEODATA_PATH, u"Impression\\Symboles"))

        # Data sources
        self.settings.setValue("Qgis/nullValue", "")
        self.settings.setValue("Qgis/addPostgisDC", True)

        # Map tools
        self.settings.setValue("Map/identifyMode", 3)
        self.settings.setValue("Map/identifyAutoFeatureForm", True)
        self.settings.setValue("Map/scales", u"1:100000,1:50000,1:25000,1:10000,1:5000,1:2500,1:1000,1:500,1:250,1:100")

        # Composer
        self.settings.setValue("Composer/defaultFont", u"Gill Sans MT")

        # Digitizing
        self.settings.setValue("Qgis/digitizing/default_snap_mode", u"to vertex and segment")
        self.settings.setValue("Qgis/digitizing/default_snapping_tolerance", 5)

        # CRS
        self.settings.setValue("Projections/otfTransformAutoEnable", False)
        self.settings.setValue("Projections/otfTransformEnabled", False)
        self.settings.setValue("Projections/projectDefaultCrs", u"EPSG:21781")
        self.settings.setValue("Projections/layerDefaultCrs", u"EPSG:21781")
        self.settings.setValue("Projections/defaultBehaviour", u"useGlobal")
        self.settings.setValue("UI/recentProjections", 1919)
        self.settings.setValue("UI/recentProjectionsProj4", u"+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +towgs84=674.4,15.1,405.3,0,0,0,0 +units=m +no_defs")
        self.settings.setValue("UI/recentProjectionsAuthId", u"EPSG:21781")

        # Network
        self.settings.setValue("proxy/proxyEnabled", True)
        self.settings.setValue("proxy/proxyHost", u"193.135.104.6")
        self.settings.setValue("proxy/proxyPort", 8080)
        self.settings.setValue("proxy/proxyType", u"HttpProxy")

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

    def __setPaths(self):

        # Favourites
        self.settings.setValue("browser/favourites", [os.path.join(self.GEODATA_PATH, u"Donnees")])

        # Last paths
        self.settings.setValue("UI/lastProjectDir", os.path.join(self.GEODATA_PATH, u"Projets"))
        self.settings.setValue("UI/lastVectorFileFilterDir", os.path.join(self.GEODATA_PATH, u"Donnees"))
        self.settings.setValue("UI/lastRasterFileFilterDir", os.path.join(self.GEODATA_PATH, u"Donnees\\Orthophotos"))
        self.settings.setValue("Qgis/last_embedded_project_path", os.path.join(self.GEODATA_PATH, u"Projets"))

    def __setWmsConnections(self):

        # ASIT VD
        self.settings.setValue("Qgis/connections-wms/ASIT VD/url", u"https://secure.asitvd.ch/proxy/ogc/asitvd-wms-fonds")
        self.settings.setValue("Qgis/connections-wms/ASIT VD/dpiMode", 7)
        self.settings.setValue("Qgis/connections-wms/ASIT VD/ignoreAxisOrientation", False)
        self.settings.setValue("Qgis/connections-wms/ASIT VD/ignoreGetFeatureInfoURI", False)
        self.settings.setValue("Qgis/connections-wms/ASIT VD/ignoreGetMapURI", False)
        self.settings.setValue("Qgis/connections-wms/ASIT VD/invertAxisOrientation", False)
        self.settings.setValue("Qgis/connections-wms/ASIT VD/smoothPixmapTransform", False)
        self.settings.setValue("Qgis/WMS/ASIT VD/username", u"vdn")

        # Vaud
        self.settings.setValue("Qgis/connections-wms/Vaud/url", u"https://secure.asitvd.ch/proxy/ogc/vd-wms")
        self.settings.setValue("Qgis/connections-wms/Vaud/dpiMode", 7)
        self.settings.setValue("Qgis/connections-wms/Vaud/ignoreAxisOrientation", False)
        self.settings.setValue("Qgis/connections-wms/Vaud/ignoreGetFeatureInfoURI", False)
        self.settings.setValue("Qgis/connections-wms/Vaud/ignoreGetMapURI", False)
        self.settings.setValue("Qgis/connections-wms/Vaud/invertAxisOrientation", False)
        self.settings.setValue("Qgis/connections-wms/Vaud/smoothPixmapTransform", False)

        # Swisstopo
        self.settings.setValue("Qgis/connections-wms/Swisstopo/url", u"http://wms.geo.admin.ch/?lang=fr")
        self.settings.setValue("Qgis/connections-wms/Swisstopo/dpiMode", 7)
        self.settings.setValue("Qgis/connections-wms/Swisstopo/ignoreAxisOrientation", False)
        self.settings.setValue("Qgis/connections-wms/Swisstopo/ignoreGetFeatureInfoURI", False)
        self.settings.setValue("Qgis/connections-wms/Swisstopo/ignoreGetMapURI", False)
        self.settings.setValue("Qgis/connections-wms/Swisstopo/invertAxisOrientation", False)
        self.settings.setValue("Qgis/connections-wms/Swisstopo/smoothPixmapTransform", False)

        # GeoPlaNet
        self.settings.setValue("Qgis/connections-wms/GeoPlaNet/url", u"http://www.geo.vd.ch/main/wsgi/mapserv_proxy")
        self.settings.setValue("Qgis/connections-wms/GeoPlaNet/dpiMode", 7)
        self.settings.setValue("Qgis/connections-wms/GeoPlaNet/ignoreAxisOrientation", False)
        self.settings.setValue("Qgis/connections-wms/GeoPlaNet/ignoreGetFeatureInfoURI", False)
        self.settings.setValue("Qgis/connections-wms/GeoPlaNet/ignoreGetMapURI", False)
        self.settings.setValue("Qgis/connections-wms/GeoPlaNet/invertAxisOrientation", False)
        self.settings.setValue("Qgis/connections-wms/GeoPlaNet/smoothPixmapTransform", False)

    def __setPlugins(self):

        # Enable plugins
        self.settings.setValue("Plugins/spatialqueryplugin", True)

        # Disable plugins
        self.settings.setValue("Plugins/grassplugin", False)
        self.settings.setValue("Plugins/roadgraphplugin", False)

        # Check updates
        self.settings.setValue("Qgis/plugin-installer/checkOnStart", True)
        self.settings.setValue("Qgis/plugin-installer/checkOnStartInterval", 7)

        # Experimental plugins
        self.settings.setValue("Qgis/plugin-installer/allowExperimental", True) # Allows experimental plugins but doesn't check the checkbox...
