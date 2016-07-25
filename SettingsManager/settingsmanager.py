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

    GEODATA_PATH = os.path.normpath("S:\\")
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
            #self.__setToolbarsVisibility()
            #self.__setPaths()
            #self.__setWmsConnections()
            #self.__setPlugins()

            self.iface.messageBar().pushMessage(u"Installation", u"Paramètres SITNyon importés (version 2.16.0.dev), redémarrer QGIS pour terminer l'installation.", level = QgsMessageBar.INFO)

    def __setOptions(self):

        settings = self.settings

        # General
        settings.setValue("Qgis/showTips216", False)
        settings.setValue("Qgis/projOpenAtLaunch", 0)
        settings.setValue("Qgis/newProjectDefault", True)

        # System
        settings.setValue("svg/searchPathsForSVG", os.path.join(self.GEODATA_PATH, "Impression\Symboles"))

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
        settings.setValue("Qgis/digitizing/default_snapping_tolerance_unit", 1)

        # CRS
        settings.setValue("Projections/otfTransformAutoEnable", False)
        settings.setValue("Projections/otfTransformEnabled", False)
        settings.setValue("Projections/projectDefaultCrs", u"EPSG:21781")
        settings.setValue("Projections/layerDefaultCrs", u"EPSG:21781")
        settings.setValue("Projections/defaultBehaviour", u"useGlobal")
        settings.setValue("UI/recentProjectionsAuthId", u"EPSG:21781")
        settings.setValue("UI/recentProjections", 1919)
        settings.setValue("UI/recentProjectionsProj4", u"+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel +towgs84=674.4,15.1,405.3,0,0,0,0 +units=m +no_defs")

        # Network
        settings.setValue("proxy/proxyEnabled", True)
        settings.setValue("proxy/proxyType", u"DefaultProxy")

    def __setToolbarsVisibility(self):

        iface = self.iface

        # Visible
        iface.attributesToolBar().setVisible(True)
        iface.digitizeToolBar().setVisible(True)
        iface.fileToolBar().setVisible(True)
        iface.layerToolBar().setVisible(True)
        iface.mapNavToolToolBar().setVisible(True)

        # Hidden
        iface.advancedDigitizeToolBar().setVisible(False)
        iface.databaseToolBar().setVisible(False)
        iface.helpToolBar().setVisible(False)
        iface.pluginToolBar().setVisible(False)
        iface.rasterToolBar().setVisible(False)
        iface.vectorToolBar().setVisible(False)
        iface.webToolBar().setVisible(False)
        iface.mainWindow().findChild(QToolBar, "mLabelToolBar").setVisible(False)

    def __setPaths(self):

        settings = self.settings

        # Favourites
        settings.setValue("browser/favourites", [os.path.join(self.GEODATA_PATH, "Donnees")])

        # Last paths
        settings.setValue("UI/lastProjectDir", os.path.join(self.GEODATA_PATH, "Projets"))
        settings.setValue("UI/lastVectorFileFilterDir", os.path.join(self.GEODATA_PATH, "Donnees"))
        settings.setValue("UI/lastRasterFileFilterDir", os.path.join(self.GEODATA_PATH, "Donnees\Orthophotos"))
        settings.setValue("Qgis/last_embedded_project_path", os.path.join(self.GEODATA_PATH, "Projets"))

        # File filter
        settings.setValue("UI/lastVectorFileFilter", "ESRI Shapefiles (*.shp *.SHP)")

    def __setWmsConnections(self):

        settings = self.settings

        # ASIT VD
        settings.setValue("Qgis/connections-wms/ASIT VD/url", u"https://secure.asitvd.ch/proxy/asitvd-wms-fonds")
        settings.setValue("Qgis/connections-wms/ASIT VD/dpiMode", 7)
        settings.setValue("Qgis/connections-wms/ASIT VD/ignoreAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/ASIT VD/ignoreGetFeatureInfoURI", False)
        settings.setValue("Qgis/connections-wms/ASIT VD/ignoreGetMapURI", False)
        settings.setValue("Qgis/connections-wms/ASIT VD/invertAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/ASIT VD/smoothPixmapTransform", False)
        settings.setValue("Qgis/WMS/ASIT VD/username", u"vdn")

        # GeoPlaNet
        settings.setValue("Qgis/connections-wms/GeoPlaNet/url", u"http://www.geo.vd.ch/main/wsgi/mapserv_proxy")
        settings.setValue("Qgis/connections-wms/GeoPlaNet/dpiMode", 7)
        settings.setValue("Qgis/connections-wms/GeoPlaNet/ignoreAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/GeoPlaNet/ignoreGetFeatureInfoURI", False)
        settings.setValue("Qgis/connections-wms/GeoPlaNet/ignoreGetMapURI", False)
        settings.setValue("Qgis/connections-wms/GeoPlaNet/invertAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/GeoPlaNet/smoothPixmapTransform", False)

        # SITNyon
        settings.setValue("Qgis/connections-wms/SITNyon/url", u"https://map.nyon.ch/prod/wsgi/mapserv_proxy")
        settings.setValue("Qgis/connections-wms/SITNyon/dpiMode", 7)
        settings.setValue("Qgis/connections-wms/SITNyon/ignoreAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/SITNyon/ignoreGetFeatureInfoURI", False)
        settings.setValue("Qgis/connections-wms/SITNyon/ignoreGetMapURI", False)
        settings.setValue("Qgis/connections-wms/SITNyon/invertAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/SITNyon/smoothPixmapTransform", False)

        settings.setValue("Qgis/connections-wms/SITNyon WMTS/url", u"https://map.nyon.ch/prod/tiles/1.0.0/WMTSCapabilities-prod.xml")
        settings.setValue("Qgis/connections-wms/SITNyon WMTS/dpiMode", 7)
        settings.setValue("Qgis/connections-wms/SITNyon WMTS/ignoreAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/SITNyon WMTS/ignoreGetFeatureInfoURI", False)
        settings.setValue("Qgis/connections-wms/SITNyon WMTS/ignoreGetMapURI", False)
        settings.setValue("Qgis/connections-wms/SITNyon WMTS/invertAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/SITNyon WMTS/smoothPixmapTransform", False)

        # Swisstopo
        settings.setValue("Qgis/connections-wms/Swisstopo/url", u"https://wms.geo.admin.ch/?lang=fr")
        settings.setValue("Qgis/connections-wms/Swisstopo/dpiMode", 7)
        settings.setValue("Qgis/connections-wms/Swisstopo/ignoreAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/Swisstopo/ignoreGetFeatureInfoURI", False)
        settings.setValue("Qgis/connections-wms/Swisstopo/ignoreGetMapURI", False)
        settings.setValue("Qgis/connections-wms/Swisstopo/invertAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/Swisstopo/smoothPixmapTransform", False)

        # Vaud
        settings.setValue("Qgis/connections-wms/Vaud/url", u"http://wms.vd.ch/public/services/VD_WMS/Mapserver/Wmsserver")
        settings.setValue("Qgis/connections-wms/Vaud/dpiMode", 7)
        settings.setValue("Qgis/connections-wms/Vaud/ignoreAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/Vaud/ignoreGetFeatureInfoURI", False)
        settings.setValue("Qgis/connections-wms/Vaud/ignoreGetMapURI", False)
        settings.setValue("Qgis/connections-wms/Vaud/invertAxisOrientation", False)
        settings.setValue("Qgis/connections-wms/Vaud/smoothPixmapTransform", False)

    def __setPlugins(self):

        settings = self.settings

        # Enable plugins
        settings.setValue("Plugins/spatialqueryplugin", True)

        # Disable plugins
        settings.setValue("Plugins/grassplugin", False)
        settings.setValue("Plugins/roadgraphplugin", False)

        # Check updates
        settings.setValue("Qgis/plugin-installer/checkOnStart", True)
        settings.setValue("Qgis/plugin-installer/checkOnStartInterval", 7)

        # Experimental plugins
        settings.setValue("Qgis/plugin-installer/allowExperimental", True) # Allows experimental plugins but doesn't check the checkbox...

        # Plugin QuickFinder
        self.__setPluginQuickFinder()

    def __setPluginQuickFinder(self):

        self.settings.setValue("PythonPlugins/quickfinder", True)
        plugin = QSettings("quickfinder_plugin", "quickfinder_plugin")

        plugin.setValue("geomapfish", True)
        plugin.setValue("geomapfishUrl", u"https://map.nyon.ch/search")
        plugin.setValue("geomapfishCrs", u"EPSG:21781")
        plugin.setValue("osm", False)
