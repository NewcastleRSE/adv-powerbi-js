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

from FileRead import fileRead

from Glyph import Glyph
from Glyph import createGlyph
from Glyph import initGlyph

#
# Code from here
#
def drawKeyGlyphs(numGlyphs, averageValue, minVariance, maxVariance, ortho):

	# copy camera collection    
    cam_x = bpy.context.scene.camera.location[0]
    cam_y = bpy.context.scene.camera.location[1]

    atX = cam_x - 1.9
    atY = cam_y + 1.2
    atZ = 1.4

    glyphRadius = 0.12
    value = 11.4
    count = 1

    minVariance = 0.0
    maxVariance = 1.0

    variance = minVariance
    varianceBounds = minVariance
    
    text_material = bpy.data.materials.get("NewWhiteEmissive");
    
    # add objects into corect colection
    scene_collection = bpy.context.view_layer.layer_collection.children['UncertaintyScale']
    bpy.context.view_layer.active_layer_collection = scene_collection   

    glyphCount = 0

    for glyphCount in range(0,5):
        #createGlyph( fname, atX, atY, atZ, mat, 0.1)
        
        glyph = initGlyph(variance, count, atX, atY, atZ, glyphRadius, value, "key-glyph-"+str(glyphCount), True)
        createGlyph( glyph, minVariance, maxVariance, ortho, numGlyphs)
        
        textZ = glyph.z1
        
        bpy.ops.object.text_add(location=(atX, atY, textZ));
        txt = bpy.context.object;
        txt.data.body = str("{:.1f}".format(varianceBounds));
        txt.data.extrude = 0.02;
        txt.data.size = 0.2;
        txt.data.materials.append(text_material);
        txt.data.align_x = 'RIGHT';
        txt.data.align_y = 'CENTER';
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY');
        txt.location=(atX + 0.38, atY, textZ);
        
        variance = variance + 0.18
        varianceBounds = varianceBounds + 0.2
        atY =  atY -0.62564
        
#for testing
#drawKeyGlyphs(5, 11.4, 0.0, 1.0, True)