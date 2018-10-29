Settings Manager
================

* [Features](#features)
    * [Options](#options)
    * [Toolbars visibility](#toolbars)
    * [Paths](#paths)
    * [Browser](#browser)
    * [WMS and WMTS connections](#wms-and-wmts-connections)
    * [PostGIS connections](#postgis-connections)
    * [Plugins](#plugins)
* [Installation](#installation)
    * [Windows](#windows)
    * [Linux](#linux)

Features
--------

**Settings Manager** is a QGIS plugin to set default settings, specific for **SITNyon** users.

### Options

| Category         | Option                                 |
| ---------------- | -------------------------------------- |
| **General**      | Do not show tips at start up           |
|                  | Do not check QGIS version at start up  |
|                  | Use default project for new project    |
| **System**       | Path for SVG symbols                   |
| **Data sources** | Representation for null values         |
|                  | Add PostGIS layers with double click   |
| **Map tools**    | Identify with layer selection          |
|                  | Open feature form if one is identified |
|                  | Predefined scales                      |
| **Composer**     | Default font                           |
|                  | Path for templates                     |
| **Digitizing**   | Default snapping mode                  |
|                  | Default snapping tolerance             |
| **CRS**          | Disable on the fly reprojection        |
|                  | Default projects CRS                   |
|                  | Default layers CRS                     |

### Toolbars

| Visible        | Hidden               |
| ------------   | -------------------- |
| Attributes     | Advanced digitizing  |
| Digitizing     | Database             |
| Manage layers  | Help                 |
| Map navigation | Label                |
| Project        | Plugins              |
|                | Raster               |
|                | Vector               |
|                | Web                  |

### Paths

* Last project
* Last vector file
* Last raster file
* Last embedded project

### Browser

* Favourites
* Hidden paths

### WMS and WMTS connections

* ASIT VD
* GeoPlaNet
* SITNyon
* Swisstopo
* Vaud

### PostGIS connections

* SITNyon
* SITNyon (developpement)
* SITNyon (formation)

### Plugins

* Check for updates on startup
* Allow experimental plugins

| Enabled       | Disabled  |
| ------------- | --------- |
| SpatialQuery  | GRASS     |
| *QuickFinder* | RoadGraph |

* Configure plugin
    * QuickFinder

[List of useful plugins](https://github.com/sitnyon/documentation/blob/master/doc/qgis-plugins.md)

Installation
------------

### Windows

Copy the folder `SettingsManager` into `%USERPROFILE%\.qgis2\python\plugins`.
> The files `Makefile`, `resources.qrc` and `ui_settingsmanager.ui` are not necessary.

Copy the file `DefaultProject/project_default.qgs` into `%USERPROFILE%\.qgis2`.

### Linux
Build the plugin with _make_:

```bash
make deploy
```
