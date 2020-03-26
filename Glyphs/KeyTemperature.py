import bpy
import os
import sys

# code to help Blender find local python modules
filepath = bpy.data.filepath
dir = os.path.dirname(filepath)
if not dir in sys.path:
   sys.path.append(dir)
      
dir = dir+'\..\Glyphs' # point to glyph code directory
if not dir in sys.path:
   sys.path.append(dir)
#----------------------------------------

from MetOffice import metOfficeLimits
from MetOffice import metOfficeColours

from Glyph import Glyph
from Glyph import createGlyph
from Glyph import initGlyph

from Glyph import Glyph
from Glyph import createGlyph
from Glyph import initGlyph

#
# Code from here
#

def drawKeyTemperature(average, ortho, text_material):

    # copy camera collection    
    cam_x = bpy.context.scene.camera.location[0]
    cam_y = bpy.context.scene.camera.location[1]
    
    # init variables
    atX = cam_x + 9.28
    atY =  cam_y + 4.5
    atZ =  1.4
    temp = 30
    r = 0.5
    
    maxY = atY

    # add objects into corect colection
    bpy.data.collections.new("TempScale")
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[-1]

    # loop    
    for x in range(1,9) :    
        name = "Temp" + str(temp)
        
        glyph = initGlyph(0.0, 10, atX, atY, 0.1, r, temp, name, True)
        createGlyph( glyph, 0.0, 1.0, ortho,1)    
        
        bpy.ops.object.text_add(location=(atX, atY, atZ));
        txt = bpy.context.object;
        txt.data.body = str(temp);
        txt.data.extrude = 0.02;
        txt.data.size = 0.5;
        txt.data.materials.append(text_material);
        txt.data.align_x = 'RIGHT';
        txt.data.align_y = 'CENTER';
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY');
        txt.location=(atX + 1.1, atY, atZ);
        
        atY =  atY - 1.355
        temp -= 5
        
    minY = atY + 0.2
    
    #print("MinY: " + str(minY))
    #print("MaxY: " + str(maxY))   
        
#for testing
#drawKeyTemperature(11.4, True)