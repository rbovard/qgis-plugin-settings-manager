Settings Manager
================

**Settings Manager** is a QGIS plugin to set default *options* and *toolbars visibility*, specific for **SITNyon** users.

### Options

| Category         | Option                                 |
| ---------------- | -------------------------------------- |
| **General**      | Show tips at start up                  |
| **System**       | Paths for SVG symbols                  |
| **Data sources** | Representation for null values         |
|                  | Add PostGIS layers with double click   |
| **Map tools**    | Open feature form if one is identified |
| **Composer**     | Default font                           |
| **Digitizing**   | Default snapping mode                  |
|                  | Default snapping tolerance             |
| **CRS**          | On the fly reprojection                |
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
