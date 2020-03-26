import bpy
import csv
import math

from Material import setMaterial
from Material import makeFlatColor

from MetOffice import metOfficeLimits
from MetOffice import metOfficeColours

from Colours import Mwhite
from Colours import Mgrey
from Colours import Mblack

import os
filePath = os.path.dirname(__file__)

class Glyph:
    def __init__(self, x, y, z1, z2, r, m, t, n, v, c):
        self.x = x
        self.y = y
        self.z1 = z1
        self.z2 = z2
        self.radius = r
        self.material = m
        self.text = t
        self.name = n
        self.variance = v
        self.count = c

#
# File Read Code
#
def fileReadVerts( fileName ):
    ifile = open(fileName)
    reader = csv.reader(ifile)

    rownum = 0
    csvTable = []
    verts=[]
    face=[]
    for row in reader:
        # Save header row.
        if rownum == 0:
            header = row
        else:
            csvTable.append(row)
            values = [float( row[1]), float(row[2]), float(row[3])]
            verts.append ( values )
            face.append( rownum - 1 )
        rownum += 1

    ifile.close()
    return (verts, face)
        
#
# Function to draw cylindrical stalk
#
def cylinder_between(x1, y1, z1, x2, y2, z2, r, gMaterial, name):

  dx = x2 - x1
  dy = y2 - y1
  dz = z2 - z1    
  dist = math.sqrt(dx**2 + dy**2 + dz**2)

  bpy.ops.mesh.primitive_cylinder_add(
      radius = r, 
      depth = dist,
      location = (dx/2 + x1, dy/2 + y1, dz/2 + z1)   
  ) 

  phi = math.atan2(dy, dx) 
  theta = math.acos(dz/dist) 

  bpy.context.object.rotation_euler[1] = theta 
  bpy.context.object.rotation_euler[2] = phi 

  bpy.context.object.name = "glyph-stalk-"+name

  newObject = bpy.context.active_object
  setMaterial(newObject, gMaterial)

#
# function to calculate glyph height
#
def initGlyph( vnce, cnt, atX, atY, atZ, r, value, name, force = False ):
    
    #Calculate sensor height
    scene = bpy.context.scene
    
    origin = ( atX, atY, 500)
    direction = (0.0,0.0,-1.0)
    
    view_layer = scene.view_layers['View Layer']
    result = scene.ray_cast(view_layer, origin, direction)
    
    if (force is not True and result[1][0]==result[1][1]==result[1][2]==0):
        print("not on model, igroring")
        return None 
    
    atZ1 = result[1][2] + atZ
    atZ2 = result[1][2]
    
    if (value is None):
        glyphValue=""
        mat = Mgrey
    else:
        i = 0
        while ( value >  metOfficeLimits[i] ):
            i += 1
        
        diffuseColour = ( float(metOfficeColours[i][0])/255.0,float(metOfficeColours[i][1])/255.0,float(metOfficeColours[i][2])/255.0, 1.0 )
        
        mat = makeFlatColor(diffuseColour, name + "-mat")
        mat = bpy.data.materials[name + "-mat"]
        
        if(value is ""):
            glyphValue=""
        else:
            glyphValue="{:.1f}".format(float(value))
    
    glyph = Glyph(atX, atY, atZ1, atZ2, r, mat, glyphValue, name, vnce, cnt)
    return glyph

#
# function to create a glyph
#
def createGlyph( glyph, minVariance, maxVariance, ortho, numGlyphs ):
    
    atX = glyph.x
    atY = glyph.y
    atZ = glyph.z1
    atZ2 = glyph.z2
    r = glyph.radius
    mat = glyph.material
    name = glyph.name
    text = glyph.text
    vnce = glyph.variance
    
    bpy.context.scene.cursor.location = (0.0, 0.0, 0.0) #set 3d cursor to origin first!!!
    
    #Draw cylinder
    if (atZ != atZ2):
        cylinder_between(atX, atY, atZ,
                            atX, atY, atZ2, r*0.02, Mwhite, name)
    
    
    # Create inner cylinder (coloured).
    bpy.ops.mesh.primitive_cylinder_add(radius = r*0.6, depth = 0.11 * r, vertices = 360)
    # Get the cylinder object and rename it.
    cyl_colour = bpy.context.object
    cyl_colour.name = 'glyph-colour-'+name
    cyl_colour.select_set(True)
    
    mat.shadow_method = 'NONE'
    setMaterial(cyl_colour, mat)
    
    if ortho==False:
        cnst = cyl_colour.constraints.new('DAMPED_TRACK')
        cnst.target = bpy.context.scene.camera
        cnst.track_axis='TRACK_Z'
    
    var_diff = maxVariance - minVariance
    increment = var_diff / numGlyphs
    
    #print("-- variance: " + str(vnce))
    
    if (vnce < 0):
        #print("-- category: error")
        fileName=filePath+"/glyphs/sxna04-08-00-0.csv"
    elif (vnce == 0.0):
        #print("-- category: 0")
        fileName=filePath+"/glyphs/sgnl00-00-00-0.csv"
    elif (vnce < increment*1):
        #print("-- category: 1")
        fileName=filePath+"/glyphs/sgnl03-00-00-0.csv"
    elif (vnce < increment*2):
        #print("-- category: 2")
        fileName=filePath+"/glyphs/sgnl06-00-00-0.csv"
    elif (vnce < increment*3):
        #print("-- category: 3")
        fileName=filePath+"/glyphs/sgnl12-00-00-0.csv"
    elif (vnce < increment*4):
        #print("-- category: 4")
        fileName=filePath+"/glyphs/sgnl24-00-00-0.csv"
    elif (vnce < increment*5):
        #print("-- category: 5")
        fileName=filePath+"/glyphs/sgnl48-00-00-0.csv"
    else: #if (vnce < 0.35):
        #print("-- category: 6")
        fileName=filePath+"/glyphs/sgnl96-00-00-0.csv"
    
    geom = fileReadVerts( fileName )
    
    glyphName = "glyph-white-"+name

    if ( vnce != 0.0 ):
        geom = fileReadVerts( fileName )

        vertsFile = geom[0]
        faceFile = [geom[1]]

        mesh_data = bpy.data.meshes.new(name)
        mesh_data.from_pydata(vertsFile, [], faceFile)
        mesh_data.update()

        cyl_white = bpy.data.objects.new(glyphName, mesh_data)
        
        view_layer = bpy.context.scene.view_layers['View Layer']
        view_layer.active_layer_collection.collection.objects.link(cyl_white)
        
        cyl_white.select_set(True)
        setMaterial(cyl_white, Mwhite)

        view_layer.objects.active = bpy.context.scene.objects[glyphName]
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[glyphName].select_set(True) # Select the default Blender Cube
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, 0, 0.045)})
        bpy.ops.object.mode_set( mode = 'OBJECT' )
        
        view_layer.objects.active.scale = (r, r, r)
        
        cyl_white.parent = cyl_colour
        
        if ortho is False:
            cyl_white = bpy.context.object
            cnst = cyl_white.constraints.new('COPY_ROTATION')
            cnst.target = bpy.context.scene.camera
            cnst = cyl_white.constraints.new('DAMPED_TRACK')
            cnst.target = bpy.context.scene.camera
            cnst.track_axis='TRACK_Z'
    else:
        # Create mid cylinder (white).
        bpy.ops.mesh.primitive_cylinder_add(radius = r*0.8, depth = 0.09 * r, vertices = 360)
        # Get the cylinder object and rename it.
        cyl_white = bpy.context.object
        cyl_white.name = glyphName
        #cyl_white.location = (atX, atY, atZ)
        cyl_white.select_set(True)
        setMaterial(cyl_white, Mwhite)
        
        cyl_white.parent = cyl_colour
        
        if ortho is False:
            cnst = cyl_white.constraints.new('DAMPED_TRACK')
            cnst.target = bpy.context.scene.camera
            cnst.track_axis='TRACK_Z'

    # Create outer cylinder (black).
    bpy.ops.mesh.primitive_cylinder_add(radius = r, depth = 0.08 * r, vertices = 360)
    # Get the cylinder object and rename it.
    cyl_black = bpy.context.object
    cyl_black.name = 'glyph-black-'+name
    #cyl_black.location = (atX, atY, atZ)
    cyl_black.select_set(True)
    setMaterial(cyl_black, Mblack)
    
    cyl_black.parent = cyl_colour
    
    cyl_colour.location = (atX, atY, atZ)
    
    if ortho is False:
        cnst = cyl_black.constraints.new('DAMPED_TRACK')
        cnst.target = bpy.context.scene.camera
        cnst.track_axis='TRACK_Z'