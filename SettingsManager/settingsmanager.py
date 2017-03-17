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

    PLUGIN_VERSION = u"2.18.0.dev"
    GEODATA_PATH = os.path.normpath("S:\\")
    PROJECTION = u"EPSG:21781"

    settings = QSettings()

    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)

        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(
            self.plugin_dir, "i18n", "settingsmanager_{}.qm" . format(locale)
        )

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > "4.3.3":
                QCoreApplication.installTranslator(self.translator)

        self.dlg = SettingsManagerDialog()

    def initGui(self):
        self.action = QAction(
            QIcon(":/plugins/settingsmanager/icon.png"), u"Settings Manager",
            self.iface.mainWindow()
        )
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
            self.__set_options()
            self.__set_toolbars_visibility()
            self.__set_paths()
            self.__set_browser()
            self.__set_wms_connections()
            self.__set_postgis_connections()
            self.__set_plugins()

            self.iface.messageBar().pushMessage(
                u"Installation",
                u"Paramètres SITNyon importés (version " + self.PLUGIN_VERSION + "), " +
                u"redémarrer QGIS pour terminer l'installation.",
                level = QgsMessageBar.INFO
            )

    def __set_options(self):

        settings = self.settings

        # General
        settings.setValue("Qgis/showTips218", False)
        settings.setValue("Qgis/checkVersion", False)
        settings.setValue("Qgis/newProjectDefault", True)

        # System
        settings.setValue(
            "svg/searchPathsForSVG",
            os.path.join(self.GEODATA_PATH, "Impression\Symboles")
        )

        # Data sources
        settings.setValue("Qgis/nullValue", "")
        settings.setValue("Qgis/addPostgisDC", True)

        # Map tools
        settings.setValue("Map/identifyMode", 3)
        settings.setValue("Map/identifyAutoFeatureForm", True)
        settings.setValue(
            "Map/scales",
            u"1:100000,1:50000,1:25000,1:10000,1:5000,1:2500,1:1000,1:500," +
            u"1:250,1:100"
        )

        # Composer
        settings.setValue("Composer/defaultFont", u"Gill Sans MT")
        settings.setValue(
            "Composer/searchPathsForTemplates",
            os.path.join(self.GEODATA_PATH, "Impression\Modeles")
        )

        # Digitizing
        settings.setValue(
            "Qgis/digitizing/default_snap_mode", u"to vertex and segment"
        )
        settings.setValue("Qgis/digitizing/default_snapping_tolerance", 5)
        settings.setValue("Qgis/digitizing/default_snapping_tolerance_unit", 1)

        # CRS
        settings.setValue("Projections/otfTransformAutoEnable", False)
        settings.setValue("Projections/otfTransformEnabled", False)
        settings.setValue("Projections/projectDefaultCrs", self.PROJECTION)
        settings.setValue("Projections/layerDefaultCrs", self.PROJECTION)
        settings.setValue("Projections/defaultBehaviour", u"useGlobal")
        settings.setValue("UI/recentProjectionsAuthId", self.PROJECTION)
        settings.setValue("UI/recentProjections", 1919) # EPSG:21781
        settings.setValue(
            "UI/recentProjectionsProj4",
            u"+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 " +
            u"+k_0=1 +x_0=600000 +y_0=200000 +ellps=bessel " +
            u"+towgs84=674.4,15.1,405.3,0,0,0,0 +units=m +no_defs"
        ) # EPSG:21781

        # Network
        settings.setValue("proxy/proxyEnabled", True)
        settings.setValue("proxy/proxyType", u"DefaultProxy")

    def __set_toolbars_visibility(self):

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
        iface.mainWindow().findChild(
            QToolBar, "mLabelToolBar"
        ).setVisible(False)
        iface.pluginToolBar().setVisible(False)
        iface.rasterToolBar().setVisible(False)
        iface.vectorToolBar().setVisible(False)
        iface.webToolBar().setVisible(False)

    def __set_paths(self):

        settings = self.settings

        # Last paths
        settings.setValue(
            "UI/lastProjectDir", os.path.join(self.GEODATA_PATH, "Projets")
        )
        settings.setValue(
            "UI/lastVectorFileFilterDir",
            os.path.join(self.GEODATA_PATH, "Donnees")
        )
        settings.setValue(
            "UI/lastRasterFileFilterDir",
            os.path.join(self.GEODATA_PATH, "Donnees\Orthophotos")
        )
        settings.setValue(
            "Qgis/last_embedded_project_path",
            os.path.join(self.GEODATA_PATH, "Projets")
        )

        # File filter
        settings.setValue(
            "UI/lastVectorFileFilter", "ESRI Shapefiles (*.shp *.SHP)"
        )

    def __set_browser(self):

        settings = self.settings

        # Favourites
        settings.setValue(
            "browser/favourites",
            [os.path.join(self.GEODATA_PATH, "Donnees")]
        )

        # Hidden paths
        settings.setValue(
            "browser/hiddenPaths",
            [
                u"S://Admin", u"S://Coordination", u"S://Documentation",
                u"S://Impression", u"S://Outils", u"A:/", u"B:/", u"C:/",
                u"D:/", u"E:/", u"F:/", u"G:/", u"H:/", u"I:/", u"J:/", u"K:/",
                u"L:/", u"M:/", u"N:/", u"O:/", u"P:/", u"Q:/", u"R:/", u"T:/",
                u"U:/", u"V:/", u"W:/", u"X:/", u"Y:/", u"Z:/"
            ]
        )

    def __set_wms_connections(self):

        settings = self.settings

        # ASIT VD
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/url",
            u"https://ows.asitvd.ch/wmts"
        )
        settings.setValue(
            "Qgis/WMS/ASIT VD/authcfg", u"asitvd1"
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/ASIT VD/smoothPixmapTransform", True
        )

        # GeoPlaNet
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/url",
            u"http://www.geo.vd.ch/main/wsgi/mapserv_proxy"
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/GeoPlaNet/smoothPixmapTransform", True
        )

        # SITNyon
        settings.setValue(
            "Qgis/connections-wms/SITNyon/url",
            u"https://map.nyon.ch/prod/wsgi/mapserv_proxy"
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon/smoothPixmapTransform", True
        )

        settings.setValue(
            "Qgis/connections-wms/SITNyon (WMTS)/url",
            u"https://map.nyon.ch/prod/tiles/1.0.0/WMTSCapabilities-prod.xml"
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon (WMTS)/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon (WMTS)/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon (WMTS)/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon (WMTS)/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon (WMTS)/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/SITNyon (WMTS)/smoothPixmapTransform", True
        )

        # Swisstopo
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/url",
            u"https://wms.geo.admin.ch/?lang=fr"
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/Swisstopo/smoothPixmapTransform", True
        )

        # Vaud
        settings.setValue(
            "Qgis/connections-wms/Vaud/url",
            u"http://wms.vd.ch/public/services/wmsVD/Mapserver/Wmsserver"
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/dpiMode", 7
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/ignoreAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/ignoreGetFeatureInfoURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/ignoreGetMapURI", False
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/invertAxisOrientation", False
        )
        settings.setValue(
            "Qgis/connections-wms/Vaud/smoothPixmapTransform", True
        )

    def __set_postgis_connections(self):

        settings = self.settings

        # SITNyon
        settings.setValue(
            "PostgreSQL/connections/SITNyon/host", u"pollux"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon/port", 5432
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon/database", u"sitnyon"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon/sslmode", 1
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon/authcfg", u"pollux1"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon/saveUsername", False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon/savePassword", False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon/geometryColumnsOnly", True
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon/dontResolveType", True
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon/publicOnly", False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon/allowGeometrylessTables", False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon/estimatedMetadata", False
        )

        # SITNyon (alcor)
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/host", u"pollux"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/port", 5432
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/database", u"sitnyon_alcor"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/sslmode", 1
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/authcfg", u"pollux1"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/saveUsername", False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/savePassword", False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/geometryColumnsOnly", True
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/dontResolveType", True
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/publicOnly", False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/allowGeometrylessTables",
            False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (alcor)/estimatedMetadata", False
        )

        # SITNyon (developpement)
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/host", u"pollux"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/port", 5432
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/database",
            u"sitnyon_developpement"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/sslmode", 1
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/authcfg", u"pollux1"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/saveUsername",
            False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/savePassword",
            False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/" +
            "geometryColumnsOnly",
            True
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/dontResolveType",
            True
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/publicOnly", False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/" +
            "allowGeometrylessTables",
            False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (developpement)/estimatedMetadata",
            False
        )

        # SITNyon (formation)
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/host", u"pollux"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/port", 5432
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/database",
            u"sitnyon_formation"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/sslmode", 1
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/authcfg", u"pollux2"
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/saveUsername", False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/savePassword", False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/geometryColumnsOnly",
            True
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/dontResolveType",
            True
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/publicOnly", False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/" +
            "allowGeometrylessTables",
            False
        )
        settings.setValue(
            "PostgreSQL/connections/SITNyon (formation)/estimatedMetadata",
            False
        )

    def __set_plugins(self):

        settings = self.settings

        # Settings
        settings.setValue("Qgis/plugin-installer/checkOnStart", True)
        settings.setValue("Qgis/plugin-installer/checkOnStartInterval", 7)
        settings.setValue(
            "Qgis/plugin-installer/allowExperimental", True
        ) # Allows experimental plugins but doesn't check the checkbox...

        # Enable plugins
        settings.setValue("Plugins/libspatialqueryplugin", True)

        # Disable plugins
        settings.setValue("Plugins/libgrassplugin7", False)
        settings.setValue("Plugins/libroadgraphplugin", False)
        settings.setValue("PythonPlugins/SettingsManager", False)

#        # Plugin ProjectLauncher
#        self.__set_plugin_project_launcher()

        # Plugin QuickFinder
        self.__set_plugin_quick_finder()

#    def __set_plugin_project_launcher(self):
#
#        settings = self.settings
#
#        # Enable plugin
#        settings.setValue("PythonPlugins/ProjectLauncher", True)
#
#        # Settings
#        settings.setValue(
#            "Plugins/ProjectLauncher/projects_list",
#            os.path.join(self.GEODATA_PATH, "Projets\projects.ini")
#        )

    def __set_plugin_quick_finder(self):

        settings = self.settings

        # Enable plugin
        settings.setValue("PythonPlugins/quickfinder", True)

        # Settings
        settings.setValue("Plugins/quickfinder_plugin/geomapfish", True)
        settings.setValue(
            "Plugins/quickfinder_plugin/geomapfishUrl",
            u"https://map.nyon.ch/search"
        )
        settings.setValue(
            "Plugins/quickfinder_plugin/geomapfishCrs", self.PROJECTION
        )
        settings.setValue("Plugins/quickfinder_plugin/osm", False)
