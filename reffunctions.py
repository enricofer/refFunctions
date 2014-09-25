# -*- coding: utf-8 -*-
"""
/***************************************************************************
ReferenceFunctions
                                 A QGIS plugin
 Provide field calculator function for Reference to other layers/features
 based on Nathan Woodrow work: 
 http://nathanw.net/2012/11/10/user-defined-expression-functions-for-qgis/
                              -------------------
        begin                : 2014-09-20
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
#from qgis.core import *
from qgis.utils import iface,qgsfunction
from qgis.core import QgsExpression,QgsMapLayer
# Import the code for the dialog
#from reffunctiondialog import refFunctionDialog
import os.path
import sys

        


@qgsfunction(4, "Reference", register=False)
def dbvalue(values, feature, parent):
    """
        Retrieve first targetField value from targetLayer when keyField is equal to conditionValue 
        
        <h4>Syntax</h4>
        <p>dqquery(<i>targetLayer,targetField,keyField,conditionValue</i>)</p>

        <h4>Arguments</h4>
        <p><i>  targetLayer</i> &rarr; the name of a currently loaded layer, for example 'myLayer'.<br>
        <i>  targetLayer</i> &rarr; a field of targetLayer whom value is needed, for example 'myTargetField'. In case of multiple results only the first is retrieved. If targetLayer = '$geometry' geometry value is retrieved <br></p>
        <i>  keyField</i> &rarr; a field of targetLayer used to search between features, for example 'myKeyField'. <br></p>
        <i>  conditionValue</i> &rarr; value used for comparisons with keyField content. Note thet the value need to be of the same type of keyField<br></p>
        
        <h4>Example</h4>
        <p><!-- Show examples of function.-->
             dbvalue('myLayer','myTargetField','myKeyField',value) <br> 
        </p>
        <h4>Notes</h4>
        <p>
             The example function is similar to dbquery('myLayer','myTargetField','myKeyField =value') , bat is significantly faster for large database
        </p>
    """
    dbg=debug()
    dbg.out("evaluating dbvalue")
    targetLayerName = values[0]
    targetFieldName = values[1]
    keyFieldName = values[2]
    contentCondition = values[3]
    if not targetLayerName in iface.legendInterface().layers():
        parent.setEvalErrorString("error: targetLayer not present")
    #iface = QgsInterface.instance()
    for layer in iface.legendInterface().layers():
        if layer.name() == targetLayerName:
            iter = layer.getFeatures()
            for feat in iter:
                if feat.attribute(keyFieldName) == contentCondition:
                    if targetFieldName == "$geometry":
                        return feat.geometry().exportToWkt()
                    else:
                        try:
                            return feat.attribute(targetFieldName)
                        except:
                            parent.setEvalErrorString("Error: invalid targetFieldName")


@qgsfunction(3, "Reference", register=False)
def dbquery(values, feature, parent):
    """
        Retrieve first targetField value from targetLayer when whereClause is true 
        
        <h4>Syntax</h4>
        <p>dqquery(<i>targetLayer,targetField,whereClause</i>)</p>

        <h4>Arguments</h4>
        <p><i>  targetLayer</i> &rarr; the name of a currently loaded layer, for example 'myLayer'.<br>
        <i>  targetLayer</i> &rarr; a field of targetLayer whom value is needed, for example 'myField'. In case of multiple results only the first is retrieved. If targetLayer = '$geometry' geometry value is retrieved <br></p>
        <i>  whereClause</i> &rarr; a valid expression string without duoble quotes to identify fields, for example 'field1 > 1 and field2 = "foo"' <br></p>
        
        <h4>Example</h4>
        <p><!-- Show examples of function.-->
             dbquery('myLayer','myField','field1 > 1 and field2 = "foo"') <br> 
             dbquery('myLayer','$geometry','field1 > 1 and field2 = "foo"') <br></p>
        
        </p>
    """
    targetLayerName = values[0].replace('"','')
    targetFieldName = values[1].replace('"','')
    whereClause = values[2].replace('"','')
    dbg=debug()
    dbg.out("evaluating dbsql")
    
    
    if not targetLayerName in iface.legendInterface().layers():
        parent.setEvalErrorString("error: targetLayer not present")
    for iterLayer in iface.legendInterface().layers():
        if iterLayer.name() == targetLayerName:
            exp = QgsExpression(whereClause)
            exp.prepare(iterLayer.dataProvider().fields())
            for feat in iterLayer.getFeatures():
                if exp.evaluate(feature):
                    if targetFieldName == "$geometry":
                        return feat.geometry().exportToWkt()
                    else:
                        try:
                            return feat.attribute(targetFieldName)
                        except:
                            parent.setEvalErrorString("Error: invalid targetField")


@qgsfunction(2, "Reference", register=False)
def dbsql(values, feature, parent):
    """
        Retrieve results from SQL query 
        
        <h4>Syntax</h4>
        <p>dbsql(<i>connectionName,sqlQuery</i>)</p>

        <h4>Arguments</h4>
        <p><i>  connectionName</i> &rarr; the name of a currently registered database connection, for example 'myConnection'.<br>
        <i>  sqlQuery</i> &rarr; a valid sql query string where do, for example 'field1 > 1 and field2 = "foo"' <br></p>
        
        <h4>Example</h4>
        <p><!-- Show examples of function.-->
             dbquery('myLayer','myField','field1 > 1 and field2 = "foo"') <br> 
             dbquery('myLayer','$geometry','field1 > 1 and field2 = "foo"') <br></p>
        
        </p>
    """
    dbg=debug()
    dbg.out("evaluating dbsql")
    connectionName = values[0]
    sqlQuery = values[1].replace('""','@#@')
    sqlQuery = sqlQuery.replace('"',"'")
    sqlQuery = sqlQuery.replace('@#@','"')
    conn = SQLconnection(connectionName)
    if conn.lastError()=="":
        res = conn.submitQuery(sqlQuery)
        dbg.out(conn.lastError())
        if conn.lastError()=="":
            if res!=[]:
                if len(res)>1 or len(res[0])>1:
                    parent.setEvalErrorString("Error: multiple results")
                else:
                    return res[0][0]
            else:
                parent.setEvalErrorString("Error: null query result")
        else:
            parent.setEvalErrorString("Error: invalid query\n"+conn.lastError())
    else:
        parent.setEvalErrorString("Error: invalid connection")

@qgsfunction(1, "Reference", register=False)
def geomRedef(values, feature, parent):
    """
        Allow to redefine current feature geometry 
        
        <h4>Syntax</h4>
        <p>dbsql(<i>geometry</i>)</p>

        <h4>Arguments</h4>
        <p><i>  geometry</i> &rarr; a valid geometry provided by expression commands 'myGeometry'.<br></p>
        
        <h4>Example</h4>
        <p><!-- Show examples of function.-->
             geomRedef('myLayer','myField','field1 > 1 and field2 = "foo"') <br> 
             dbquery('myLayer','$geometry','field1 > 1 and field2 = "foo"') <br></p>
        
        </p>
    """
    dbg=debug()
    dbg.out("self redefine geometry")
    targetGeometry = values[0]
    if iface.mapCanvas().currentLayer().isEditable():
        try:
            iface.mapCanvas().currentLayer().changeGeometry(feature.id(), targetGeometry)
            #iface.mapCanvas().currentLayer().updateExtents()
            #iface.mapCanvas().currentLayer().setCacheImage(None)
            iface.mapCanvas().currentLayer().triggerRepaint()
            #feature.setGeometry(targetGeometry)
            return 1
        except:
            parent.setEvalErrorString("Error: geometry is not valid")
            return 0

@qgsfunction(1, "Reference", register=False)
def xx(values, feature, parent):
    """
        Return the coordinate x of the given point geometry 
        
        <h4>Syntax</h4>
        <p>dbsql(<i>geometry</i>)</p>

        <h4>Arguments</h4>
        <p><i>  geometry</i> &rarr; a valid geometry provided by expression commands 'myGeometry'.<br></p>
        
        <h4>Example</h4>
        <p><!-- Show examples of function.-->
             geomRedef('myLayer','myField','field1 > 1 and field2 = "foo"') <br> 
             dbquery('myLayer','$geometry','field1 > 1 and field2 = "foo"') <br></p>
        
        </p>
    """
    dbg=debug()
    dbg.out("xx")
    refFeat = QgsGeometry()
    refFeat.fromWkt(value[0])
    if refFeat.type()==Qgis.Point:
        return refFeat.asPoint().x()
    else:
        parent.setEvalErrorString("Error: Invalid point geometry")

@qgsfunction(1, "Reference", register=False)
def yy(values, feature, parent):
    """
        Return the coordinate x of the given point geometry 
        
        <h4>Syntax</h4>
        <p>dbsql(<i>geometry</i>)</p>

        <h4>Arguments</h4>
        <p><i>  geometry</i> &rarr; a valid geometry provided by expression commands 'myGeometry'.<br></p>
        
        <h4>Example</h4>
        <p><!-- Show examples of function.-->
             geomRedef('myLayer','myField','field1 > 1 and field2 = "foo"') <br> 
             dbquery('myLayer','$geometry','field1 > 1 and field2 = "foo"') <br></p>
        
        </p>
    """
    dbg=debug()
    dbg.out("yy")
    refFeat = QgsGeometry()
    refFeat.fromWkt(value[0])
    if refFeat.type()==Qgis.Point:
        return refFeat.asPoint().y()
    else:
        parent.setEvalErrorString("Error: Invalid point geometry")

@qgsfunction(1, "dbExpressions", register=False)
def centroid(values, feature, parent):
    """
        Return the centroid of the given geometry 
        
        <h4>Syntax</h4>
        <p>dbsql(<i>geometry</i>)</p>

        <h4>Arguments</h4>
        <p><i>  geometry</i> &rarr; a valid geometry provided by expression commands 'myGeometry'.<br></p>
        
        <h4>Example</h4>
        <p><!-- Show examples of function.-->
             geomRedef('myLayer','myField','field1 > 1 and field2 = "foo"') <br> 
             dbquery('myLayer','$geometry','field1 > 1 and field2 = "foo"') <br></p>
        
        </p>
    """
    dbg=debug()
    dbg.out("centroid")
    refFeat = QgsGeometry()
    refFeat.fromWkt(value[0])
    if refFeat.isGeosValid():
        return refFeat.exportToWkt()
    else:
        parent.setEvalErrorString("Error: Invalid geometry")
        

@qgsfunction(1, "Reference", register=False)
def lenght(values, feature, parent):
    """
        Return the length of the given geometry 
        
        <h4>Syntax</h4>
        <p>dbsql(<i>geometry</i>)</p>

        <h4>Arguments</h4>
        <p><i>  geometry</i> &rarr; a valid geometry provided by expression commands 'myGeometry'.<br></p>
        
        <h4>Example</h4>
        <p><!-- Show examples of function.-->
             geomRedef('myLayer','myField','field1 > 1 and field2 = "foo"') <br> 
             dbquery('myLayer','$geometry','field1 > 1 and field2 = "foo"') <br></p>
        
        </p>
    """
    dbg=debug()
    dbg.out("lenght")
    refFeat = QgsGeometry()
    refFeat.fromWkt(value[0])
    return refFeat.lenght()
    

@qgsfunction(1, "Reference", register=False)
def area(values, feature, parent):
    """
        Return the area of the given geometry 
        
        <h4>Syntax</h4>
        <p>dbsql(<i>geometry</i>)</p>

        <h4>Arguments</h4>
        <p><i>  geometry</i> &rarr; a valid geometry provided by expression commands 'myGeometry'.<br></p>
        
        <h4>Example</h4>
        <p><!-- Show examples of function.-->
             geomRedef('myLayer','myField','field1 > 1 and field2 = "foo"') <br> 
             dbquery('myLayer','$geometry','field1 > 1 and field2 = "foo"') <br></p>
        
        </p>
    """
    dbg=debug()
    dbg.out("area")
    refFeat = QgsGeometry()
    refFeat.fromWkt(value[0])
    return refFeat.area()

@qgsfunction(0,"Reference", register=False)
def nearestVertex(values, feature, parent):
    """
        Return the nearest vertex as point geometry
        
        <h4>Syntax</h4>
        <p>dbsql(<i>geometry</i>)</p>

        <h4>Arguments</h4>
        <p><i>  geometry</i> &rarr; a valid geometry provided by expression commands 'myGeometry'.<br></p>
        
        <h4>Example</h4>
        <p><!-- Show examples of function.-->
             geomRedef('myLayer','myField','field1 > 1 and field2 = "foo"') <br> 
             dbquery('myLayer','$geometry','field1 > 1 and field2 = "foo"') <br></p>
        
        </p>
    """
    dbg=debug()
    dbg.out("nearestVertex")
    pass            

@qgsfunction(2, "Reference", register=False)
def dbnearest(values, feature, parent):
    """
        Retrieve results from SQL query 
        
        <h4>Syntax</h4>
        <p>dbsql(<i>connectionName,sqlQuery</i>)</p>

        <h4>Arguments</h4>
        <p><i>  connectionName</i> &rarr; the name of a currently registered database connection, for example 'myConnection'.<br>
        <i>  sqlQuery</i> &rarr; a valid sql query string where do, for example 'field1 > 1 and field2 = "foo"' <br></p>
        
        <h4>Example</h4>
        <p><!-- Show examples of function.-->
             dbquery('myLayer','myField','field1 > 1 and field2 = "foo"') <br> 
             dbquery('myLayer','$geometry','field1 > 1 and field2 = "foo"') <br></p>
        
        </p>
    """
    dbg=debug()
    dbg.out("evaluating dbnearest")
    targetLayerName = values[0]
    targetFieldName = values[1]
    dmin = sys.float_info.max
    dbg.out(feature)
    actualGeom = feature.geometry()
    if not (targetLayerName in [layer.name() for layer in iface.legendInterface().layers()]):
        parent.setEvalErrorString("error: targetLayer not present")
        return
    count = 0
    for layer in iface.legendInterface().layers():
        if layer != iface.mapCanvas().currentLayer() and layer.type() == QgsMapLayer.VectorLayer and (targetLayerName == '' or layer.name() == targetLayerName ):
            dbg.out(layer.name())
            iter = layer.getFeatures()
            for feat in iter:
                dtest = actualGeom.distance(feat.geometry())
                count += 1
                if count < 100000:
                    if dtest<dmin:
                        dmin = dtest
                        if targetFieldName=="$geometry":
                            dminRes = feat.geometry().exportToWkt()
                        elif targetFieldName=="$vertex":
                            dminRes = feat.geometry().closestVertex(actualGeom.centroid().asPoint()).wellKnownText()
                        elif targetFieldName=="$distance":
                            dminRes = dmin
                        else:
                            try:
                                dminRes = feat.attribute(targetFieldName)
                            except:
                                parent.setEvalErrorString("error: targetFieldName not present")
                                return
                else:
                    parent.setEvalErrorString("error: too many features to compare")
    dbg.out("DMIN")
    dbg.out(dmin)
    if count > 0:
        return dminRes
    else:
        parent.setEvalErrorString("error: no features to compare")

def stringToPythonNames(string):
        validPyChars="1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM_"
        stringOK=""
        for char in string.encode('ascii', 'ignore'):
            if char in validPyChars:
                stringOK += char
        return "layer_"+stringOK

def registerLayers():
    dbg=debug()
    dbg.out("register layer names")
    dbg.out("layers loaded")
    dbg.out(iface.mapCanvas().layers())
    for layer in iface.legendInterface().layers():
        if layer.type() == QgsMapLayer.VectorLayer:
            layerNameOK = stringToPythonNames(layer.name())
            dbg.out(layerNameOK)
            layerCode = """
@qgsfunction(0, "Reference", register=False)
def %s(values, feature, parent):
    return '%s'""" % (layerNameOK,layer.name().encode('ascii', 'ignore'))
            dbg.out(layerCode)
            #exec layerCode
            #QgsExpression.registerFunction(locals()[layerNameOK])
    dbg.out(locals())

def unregisterLayers():
    dbg=debug()
    dbg.out("unregister layer names")
    for layer in iface.legendInterface().layers():
        if layer.type() == QgsMapLayer.VectorLayer:
            #QgsExpression.unregisterFunction(stringToPythonNames(layer.name()))
            dbg.out(stringToPythonNames(layer.name()))
    dbg.out(locals())

class debug:

    def __init__(self):
        self.debug = True
        
    def out(self,string):
        if self.debug:
            print string

class SQLconnection:

    def __init__(self,conn):
        self.dbg = debug()
        s = QSettings()
        s.beginGroup("PostgreSQL/connections/"+conn)
        currentKeys = s.childKeys()
        self.PSQLDatabase=s.value("database", "" )
        self.PSQLHost=s.value("host", "" )
        self.PSQLUsername=s.value("username", "" )
        self.PSQLPassword=s.value("password", "" )
        self.PSQLPort=s.value("port", "" )
        self.PSQLService=s.value("service", "" )
        s.endGroup()
        self.db = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName(self.PSQLHost)
        self.db.setPort(int(self.PSQLPort))
        self.db.setDatabaseName(self.PSQLDatabase)
        self.db.setUserName(self.PSQLUsername)
        self.db.setPassword(self.PSQLPassword)
        ok = self.db.open()
        if not ok:
            self.error = "Database Error: %s" % self.db.lastError().text()
            #QMessageBox.information(None, "DB ERROR:", error)
        else:
            self.error=""

    def submitQuery(self,sql):
        query = QSqlQuery(self.db)
        query.exec_(sql)
        self.dbg.out(sql)
        rows= []
        self.dbg.out("SQL RESULT:")
        self.dbg.out(query.lastError().type())
        self.dbg.out(query.lastError().text())
        if query.lastError().type() != QSqlError.NoError:
            self.error = "Database Error: %s" % query.lastError().text()
            #QMessageBox.information(None, "SQL ERROR:", resultQuery) 
        else:
            self.error = ""
            while (query.next()):
                fields=[]
                count = 0
                #query.value(count)
                for k in range(0,query.record().count()):
                    try:
                        fields.append(unicode(query.value(k), errors='replace'))
                    except TypeError:
                        fields.append(query.value(k))
                    except AttributeError:
                        fields.append(str(query.value(k)))
                rows += [fields]
        self.dbg.out(rows)
        return rows

    def lastError(self):
        return self.error

class refFunctions:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        self.dbg = debug()

        # Create the dialog (after translation) and keep reference
        #self.dlg = refFunctionDialog()

        
    def initGui(self):
        self.dbg.out("initGui")
        registerLayers()
        
        #QgsExpression.registerFunction(EL_DIV)
        QgsExpression.registerFunction(dbvalue)
        QgsExpression.registerFunction(dbquery)
        QgsExpression.registerFunction(dbsql)
        QgsExpression.registerFunction(dbnearest)
        QgsExpression.registerFunction(geomRedef)
        QgsExpression.registerFunction(xx)
        QgsExpression.registerFunction(yy)
        QgsExpression.registerFunction(lenght)
        QgsExpression.registerFunction(area)
        QgsExpression.registerFunction(centroid)
        # Create action that will start plugin configuration
        #self.action = QAction(
        #    QIcon(":/plugins/multiprint/icon.png"),
        #    u"print multiple print composer views", self.iface.mainWindow())
        # connect the action to the run method
        #self.dlg.path.setText(QDesktopServices.storageLocation ( QDesktopServices.DocumentsLocation ))
        #self.dlg.checkBox.stateChanged.connect(self.selectAllCheckbox)
        #self.dlg.exportAsPdf.clicked.connect(self.pdfOut)
        #self.dlg.exportAsImg.clicked.connect(self.imgOut)
        #self.dlg.browse.clicked.connect(self.browseDir)
        #self.action.triggered.connect(self.run)
        # Add toolbar button and menu item
        #self.iface.addToolBarIcon(self.action)
        #self.iface.addPluginToMenu(u"&multiPrint", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        #self.iface.removePluginMenu(u"&multiPrint", self.action)
        #self.iface.removeToolBarIcon(self.action)
        unregisterLayers()
        QgsExpression.unregisterFunction('dbvalue')
        QgsExpression.unregisterFunction('dbquery')
        QgsExpression.unregisterFunction('dbsql')
        QgsExpression.unregisterFunction('dbnearest')
        QgsExpression.unregisterFunction('geomRedef')
        QgsExpression.unregisterFunction('xx')
        QgsExpression.unregisterFunction('yy')
        QgsExpression.unregisterFunction('lenght')
        QgsExpression.unregisterFunction('area')
        QgsExpression.unregisterFunction('centroid')


