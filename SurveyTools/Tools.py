'''
Created on 3 oct. 2015

@author: albert
'''
import FreeCAD
from PySide import QtGui,QtCore
import FreeCADGui, easygui


def getMainWindow():
    "returns the main window"
    # using QtGui.qApp.activeWindow() isn't very reliable because if another
    # widget than the mainwindow is active (e.g. a dialog) the wrong widget is
    # returned
    toplevel = QtGui.qApp.topLevelWidgets()
    for i in toplevel:
        if i.metaObject().className() == "Gui::MainWindow":
            return i
    raise Exception("No main window found")

def getComboView(mw):
    dw=mw.findChildren(QtGui.QDockWidget)
    for i in dw:
        if str(i.objectName()) == "Combo View":
            return i.findChild(QtGui.QTabWidget)
        elif str(i.objectName()) == "Python Console":
            return i.findChild(QtGui.QTabWidget)
    raise Exception ("No tab widget found")


def creaCarpeta(name='nom'):
    '''
    Check if a group with designed name exists or create one 
    and return it 
    '''
    
    
    doc = FreeCAD.activeDocument()
    for obj in doc.Objects:
        if obj.Label == name:
            if  obj.TypeId == 'App::DocumentObjectGroup':
                return obj
    
    grp = doc.addObject("App::DocumentObjectGroup", name )
    return grp

def crearPunt(name = "Point",X=0, Y=0,Z=0, Code = '', size= 5):
    ''' creaPunt(name, x,y,z ,code, size) or 
        creaPunt(Vector,name, code, size)
        create a Point with custom name and code
    '''
    obj=FreeCAD.ActiveDocument.addObject("Part::FeaturePython",str(name))   #create a object with your name
    if isinstance(X,FreeCAD.Vector):      # if a Vector is  passed assigns values to x,y,z              
        Z = X.z
        Y = X.y
        X = X.x
    Punt(obj,name, X,Y,Z,Code)              #creates the object
    obj.X = X
    obj.Y = Y
    obj.Z = Z
    
    obj.ViewObject.PointSize = size         # asigns the size point
    obj.ViewObject.Proxy =0
    FreeCAD.ActiveDocument.recompute()
    return obj


class Punt():
    "Punt de topografia"
    def __init__(self, obj,name=None,x=0,y=0,z=0, c=None):
        #adding the object properties
        obj.Label = str(name)                                   
        obj.addProperty("App::PropertyString","Tipus","Propietats","Descripcio").Tipus = 'Punt'
        obj.addProperty("App::PropertyString","Codi","Base","Descripcio").Codi = str(c)
        obj.addProperty("App::PropertyFloat","X","Coordenades","Location").X = float(x)
        obj.addProperty("App::PropertyFloat","Y","Coordenades","Location").Y = float(y)
        obj.addProperty("App::PropertyFloat","Z","Coordenades","Location").Z = float(z)
        
        #hiding the properties Tipus and placement
        mode = 2
        obj.setEditorMode('Placement',mode)
        obj.setEditorMode("Tipus", mode)
        obj.Proxy= self
        

    def __getstate__(self):
        return self.Type

    def __setstate__(self,state):
        if state:
            self.Type = state  
            
    def execute(self, obj):
        import Part                         
        punt = Part.Vertex(FreeCAD.Vector(obj.X,obj.Y,obj.Z))
        obj.Shape = punt
        
    def onChanged(self, obj, prop):
        pass 
    
    
def creaSuperficie(name='superficie', punts=[],linies=None):
    '''
    crea un objecte superficie
    '''
    doc = FreeCAD.activeDocument()
    obj = doc.addObject('App::DocumentObjectGroupPython',name)
    Superficie(obj, name)
    FreeCAD.ActiveDocument.recompute()
    return obj

def selectPointsGroup(codes_dict=False):
    '''
    select all point in a group
    @return: If a point group is selected return this group, if anything is selected return all groups of points
    '''
    sel = FreeCADGui.Selection.getSelection()
    
    
    if len(sel)>0:
        if sel[0].InList[0].Tipus != "Punts":
            
            easygui.msgbox("Selecciona una carpeta de punts o res per seleccionar tots els punts", 'Instruccions')
        elif sel[0].Group[0].Tipus != "Punt":
            easygui.msgbox("la carpeta ha de contenir punts ", 'Instruccions')

    else:
        doc = FreeCAD.activeDocument()
        if len(doc.Punts.Group)>0:
            for grp in doc.Punts.Group:
                    
                sel.append(grp)
                
        else:
            easygui.msgbox("No hi hsn punts, fes servir l'eina importar", 'Instruccions')
               
                   
    punts =None
    if not codes_dict:
        punts =[]
        for g in sel:
            for punt in g.Group:
                punts.append(punt)
    else:
        punts = set()
        for g in sel:
            for punt in g.Group:
                Code = punt.Codi.split(',')
                for c in Code:
                    if not c[-2:] == ' I':
                        punts.add(c)
        
                    
    return punts
    
    
    
def getTxtTriangle(punts=None, linies = None):
    '''
    It creats a list of vectors an a list of edges
    @return: return a strin for a triangle file 
                if edges *.poly
                if only points *.nodes
                
                
              #  First line: <# of vertices> <dimension (must be 2)> <# of attributes> <# of boundary markers (0 or 1)>
              #  Following lines: <vertex #> <x> <y> [attributes] [boundary marker]
              #  One line: <# of segments> <# of boundary markers (0 or 1)>
              #  Following lines: <segment #> <endpoint> <endpoint> [boundary marker]
              #  One line: <# of holes>
              #  Following lines: <hole #> <x> <y>
              #  Optional line: <# of regional attributes and/or area constraints>
              #  Optional following lines: <region #> <x> <y> <attribute> <maximum area> 
    '''
    if punts ==None:
        punts=selectPointsGroup()
    txt = ""
    txt += str(len(punts))+'\t'+'1'
    if linies !=None :
        txt += '\t1\n'
    else:
        txt += '\t0\n'
    num_p = 0
    for p in punts:
        if linies !=None :
            txt += num_p+'\t'+p.X+'\t'+p.Y+'\t'+p.Z+'\n'
        else:
            txt += num_p+'\t'+p.X+'\t'+p.Y+'\t'+p.Z+'\n'
    return txt
    
    
class Superficie():
    "objecte superficie"
    def __init__(self, obj,name='Sup', punts=[],linies=[]):
        #adding the object properties
        obj.Label = str(name)                
        obj.addProperty("App::PropertyString","Tipus","Propietats","Descripcio").Tipus = 'Superficie'
                   
        obj.addProperty("App::PropertyVectorList","Punts","Definition",'llista de pnts').Punts = punts
        obj.addProperty("App::PropertyVectorList","Linies","Definition",'llista de linies').Linies = linies
        obj.addProperty("App::PropertyVectorList","Triangles","Definition",'llista de triangles').Triangles = []
        self.Type='Superficie'
        mode = 2
        obj.setEditorMode("Tipus", mode)
        obj.Proxy= self
        
        

    def __getstate__(self):
        return self.Type

    def __setstate__(self,state):
        if state:
            self.Type = state  
            
    def execute(self, obj):
        pass
        
    def onChanged(self, obj, prop):
        pass 
