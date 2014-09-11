Settings Manager
================

**Settings Manager** is a QGIS plugin to set default settings, specific for **SITNyon** users:
* Options
* Toolbars visibility
* Paths
* WMS connections
* Plugins settings

### Options

| Category         | Option                                 |
| ---------------- | -------------------------------------- |
| **General**      | Don't show tips at start up            |
| **System**       | Paths for SVG symbols                  |
| **Data sources** | Representation for null values         |
|                  | Add PostGIS layers with double click   |
| **Map tools**    | Identify with layer selection          |
|                  | Open feature form if one is identified |
| **Composer**     | Default font                           |
| **Digitizing**   | Default snapping mode                  |
|                  | Default snapping tolerance             |
| **CRS**          | Disable on the fly reprojection        |
|                  | Default projects CRS                   |
|                  | Default layers CRS                     |
| **Network**      | Use proxy for web access               |

### Toolbars

| Visible        | Hidden               |
| ------------   | -------------------- |
| Attributes     | Advanced digitizing  |
| Digitizing     | Database             |
| File           | Help                 |
| Manage layers  | Label                |
| Map navigation | Plugins              |
|                | Raster               |
|                | Vector               |
|                | Web                  |

### Paths

* Favourites
* Last project
* Last vector file
* Last raster file
* Last embedded project

### WMS connections

* ASIT VD
* Vaud

### Plugins settings

* Allow experimental plugins

Installation
------------

### Windows

Copy the folder `SettingsManager` into `C:\Users\<username>\.qgis2\python\plugins`.
> The files `Makefile`, `resources.qrc` and `ui_settingsmanager.ui` are not necessary.

### Linux
Build the plugin with Makefile:

```bash
make deploy
```
