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
from Glyph import getGlyphMaterial

#
# Code from here
#

def drawKey(average, key_type, max_value, ortho, text_material):

    # copy camera collection    
    cam_x = bpy.context.scene.camera.location[0]
    cam_y = bpy.context.scene.camera.location[1]
    
    # init variables
    atX = cam_x + 9.28
    atY =  cam_y + 4.5
    atZ =  1.4
    r = 0.5
    
    maxY = atY

    # add objects into corect colection
    bpy.data.collections.new("TempScale")
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children[-1]

    # loop    
    if (key_type == "metTemp"):
        v = 30
        for x in range(1,9) :    
            name = "Value" + str(v)
            
            glyphMat = getGlyphMaterial(v, max_value, key_type)
            glyph = initGlyph(0.0, 10, (atX, atY, 0.1), r, v, glyphMat, name, True)
            createGlyph( glyph, 0.0, 1.0, ortho, 1)    
            
            bpy.ops.object.text_add(location=(atX, atY, atZ));
            txt = bpy.context.object;
            txt.data.body = str(v);
            txt.data.extrude = 0.02;
            txt.data.size = 0.5;
            txt.data.materials.append(text_material);
            txt.data.align_x = 'RIGHT';
            txt.data.align_y = 'CENTER';
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY');
            txt.location=(atX + 1.1, atY, atZ);
            
            atY =  atY - 1.355
            v -= 5
    elif (key_type == "covid19"):
        v = max_value    

        v_diff = max_value / 5
        v = max_value - (v_diff * 0.5)
        
        if (max_value > 1000000):
            text = [
                str("> %.2f" % ((max_value - v_diff)/1000000))+"M",
                "> "+str("%.2f" % ((max_value - v_diff*2)/1000000))+"M",
                "> "+str("%.2f" % ((max_value - v_diff*3)/1000000))+"M",
                "> "+str("%.2f" % ((max_value - v_diff*4)/1000000))+"M",
                "< "+str("%.2f" % ((max_value - v_diff*4)/1000000))+"M"
            ]
        elif (max_value > 100000):
            text = [
                str("> %.1f" % ((max_value - v_diff)/1000))+"k",
                "> "+str("%.1f" % ((max_value - v_diff*2)/1000))+"k",
                "> "+str("%.1f" % ((max_value - v_diff*3)/1000))+"k",
                "> "+str("%.1f" % ((max_value - v_diff*4)/1000))+"k",
                "< "+str("%.1f" % ((max_value - v_diff*4)/1000))+"k"
            ]
        else:
            text = [
                str("> %.0f" % (max_value - v_diff)),
                "> "+str("%.0f" % (max_value - v_diff*2)),
                "> "+str("%.0f" % (max_value - v_diff*3)),
                "> "+str("%.0f" % (max_value - v_diff*4)),
                "< "+str("%.0f" % (max_value - v_diff*4))
            ]
        
        for x in range(1,6) :    
            name = "Value" + str(v)
            
            glyphMat = getGlyphMaterial(v, max_value, key_type)
            glyph = initGlyph(0.0, 10, (atX, atY, 0.1), r, v, glyphMat, name, True)
            createGlyph( glyph, 0.0, 1.0, ortho, 1)    
            
            bpy.ops.object.text_add(location=(atX, atY, atZ));
            txt = bpy.context.object;
            txt.data.body = text[x-1];
            txt.data.extrude = 0.02;
            txt.data.size = 0.3;
            txt.data.materials.append(text_material);
            txt.data.align_x = 'RIGHT';
            txt.data.align_y = 'CENTER';
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY');
            txt.location=(atX + 1.1, atY, atZ);
            
            atY =  atY - 1.8
            v -= v_diff
        
    minY = atY + 0.2
    
    #print("MinY: " + str(minY))
    #print("MaxY: " + str(maxY))   
        
#for testing
#drawKeyTemperature(11.4, True)