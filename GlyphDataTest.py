import bpy
import bmesh
from mathutils import Vector
import csv
import os
import glob
import math
import sys
import json

from random import *

# code to help Blender find local python modules
filepath = bpy.data.filepath
dir = os.path.dirname(filepath)

if not dir in sys.path:
   sys.path.append(dir)
      
dir = dir+'\Glyphs' # point to glyph code directory
if not dir in sys.path:
   sys.path.append(dir)
#----------------------------------------

from Material import makeFlatColor
from Material import makeEmissive
from Material import makeEmissiveAlpha

from Glyph import Glyph
from Glyph import createGlyph
from Glyph import initGlyph
from Glyph import getGlyphMaterial

from Key import drawKey

from latlonTOukng import WGS84toOSGB36

E_adj = -424500
N_adj = -564500

# Detect current working directory -------
currentDir = os.path.dirname(__file__)
strs = currentDir.split("\\")

if ".blend" in strs[len(strs)-1]:
    currentDir = ""
    x = 0
    for strng in strs:
        currentDir = currentDir + strng
        currentDir = currentDir + "\\"
        x = x + 1
        
        if x == (len(strs) - 1):
            break

os.chdir( currentDir )
print( os.getcwd() )

#--------------------------------------------------------------

text_material = bpy.data.materials.get("Text");
bg_colour = bpy.data.materials.get("BG-Material");

axis_colour = text_material
axis_value_colour = text_material
axis_label_colour = text_material
gridlines_colour = text_material

axes_z = -0.5

x_axis_length = 12.5

start_x = -5.5
end_x = start_x + x_axis_length

y_axis_length = 9.5

start_y = -4.25
end_y = start_y + y_axis_length

x_axis_values = []
y_axis_values = []

properties = None

def hextofloats(h, a):
    floats = [int(h[i:i + 2], 16) / 255. for i in (0, 2, 4)]
    floats.append(a)
    return floats

def drawYAxis(min, max, inc, y_axis_label):
    idx = min;
       
    if (inc==0.0):
        y_axis_values.append(min-1)
        y_axis_values.append(min)
        y_axis_values.append(min+1)
    else:
        y_axis_values.append(min - inc)
        
        while idx <= max:
            y_axis_values.append(idx);
            idx += inc;
        
        #y_axis_values.append(max)
        y_axis_values.append(max + inc)
    
    num_items = len(y_axis_values);
    index = 0;
    increment = y_axis_length/(num_items-1);
    
    for y in y_axis_values:    
        bpy.ops.object.text_add(location=(-6.0, start_y+(index*increment)-0.125, axes_z));
        txt = bpy.context.object;
        txt.data.body = str(round(y,2));
        txt.data.extrude = 0.02;
        txt.data.size = 0.4;
        txt.data.align_x = 'RIGHT';
        txt.data.materials.append(axis_value_colour);
        
        if(index!=0):
            bpy.ops.mesh.primitive_cube_add(location=(0.7, start_y+(index*increment), axes_z));
            cube = bpy.context.object;
            cube.dimensions = (x_axis_length+0.1,0.01,0.01);
            
            cube.data.materials.append(gridlines_colour);
        else:
            bpy.ops.mesh.primitive_cube_add(location=(0.75, start_y+(index*increment), axes_z));
            cube = bpy.context.object;
            cube.dimensions = (x_axis_length+0.25,0.05,0.01);
            cube.data.materials.append(axis_colour);
        
        index = index + 1;
    
    #axis label    
    bpy.ops.object.text_add(location=(-7.45, 0.0, axes_z));
    txt = bpy.context.object;
    txt.data.body = y_axis_label;
    txt.data.extrude = 0.02;
    txt.data.size = 0.5;
    txt.rotation_euler = (0.0, 0.0, 1.5708);        #radians!
    txt.data.materials.append(axis_label_colour);
    txt.data.align_x = 'CENTER';

def drawXAxis(min, max, inc, x_axis_label):
    idx = min;
    
    if (inc==0.0):
        x_axis_values.append(min-1)
        x_axis_values.append(min)
        x_axis_values.append(min+1)
    else:
        x_axis_values.append(min - inc)
        
        while idx <= max:
            x_axis_values.append(idx);
            idx += inc;
            
        #x_axis_values.append(max)
        x_axis_values.append(max + inc)
    
    num_items = len(x_axis_values);
    index = 0;
    increment = x_axis_length/(num_items-1);
    
    for x in x_axis_values:    
        bpy.ops.object.text_add(location=(start_x+(index*increment), -5.0, axes_z));
        txt = bpy.context.object;
        txt.data.body = str(round(x,2));
        txt.data.extrude = 0.02;
        txt.data.size = 0.4;
        txt.data.align_x = 'CENTER';
        txt.data.materials.append(axis_value_colour);
        
        if(index!=0):
            bpy.ops.mesh.primitive_cube_add(location=(start_x+(index*increment), 0.45, axes_z));
            cube = bpy.context.object;
            cube.dimensions = (0.01,y_axis_length+0.1,0.01);
            cube.data.materials.append(gridlines_colour);
        else:
            bpy.ops.mesh.primitive_cube_add(location=(start_x+(index*increment), 0.5, axes_z));
            cube = bpy.context.object;
            cube.dimensions = (0.05,y_axis_length+0.25,0.01);
            cube.data.materials.append(axis_colour);
        
        index = index + 1;
    
    #axis label    
    bpy.ops.object.text_add(location=(0, -5.5, axes_z));
    txt = bpy.context.object;
    txt.data.body = x_axis_label;
    txt.data.extrude = 0.02;
    txt.data.size = 0.5;
    txt.data.materials.append(axis_label_colour);
    txt.data.align_x = 'CENTER';
    txt.data.align_y = 'CENTER';

minVariance = 0.0
maxVariance = 1.0

ortho = True

numGlyphs = 7

min_x = None
max_x = None 
min_y = None
max_y = None

##----------------------------------------- Code from here

# LOAD JSON DATA
argv = sys.argv             
argv = argv[argv.index("--") + 1:]  # get all args after "--"

j_data = json.loads(argv[0])
values = j_data["data"]

background = j_data["background"]
glyph_scale = float(j_data["glyph_scale"])
    
ax_col = hextofloats(j_data['graph_settings']['axis_colour'], 1.0)
axis_colour = makeEmissive(ax_col, 'AxisMaterial')
axis_colour = bpy.data.materials['AxisMaterial']

tx_col = hextofloats(j_data['graph_settings']['label_colour'], 1.0)
axis_value_colour = makeEmissive(tx_col, 'AxisValueMaterial')
axis_value_colour = bpy.data.materials['AxisValueMaterial']

ax_col = hextofloats(j_data['graph_settings']['text_colour'], 1.0)
axis_label_colour = makeEmissive(ax_col, 'AxisLabelMaterial')
axis_label_colour = bpy.data.materials['AxisLabelMaterial']

gx_col = hextofloats(j_data['graph_settings']['gridline_colour'], 1.0)
gridlines_colour = makeEmissive(gx_col, 'GridlinesMaterial')
gridlines_colour = bpy.data.materials['GridlinesMaterial']

bg_col = hextofloats(j_data['graph_settings']['background_colour'], 0.85)
bg_colour = makeEmissiveAlpha(bg_col, 'New-BG-Material')
bg_colour = bpy.data.materials['New-BG-Material']
bg_colour.blend_method = 'BLEND'

bpy.data.objects["Plane"].data.materials[0] = bg_colour         
bpy.data.objects["Plane.001"].data.materials[0] = bg_colour
bpy.data.objects["Plane.002"].data.materials[0] = bg_colour

if background == "map":
    bpy.data.objects["Plane"].hide_render = True
    bpy.data.collections['Background'].hide_render = False
else:
    bpy.data.objects["Plane"].hide_render = False
    bpy.data.collections['Background'].hide_render = True

bpy.data.objects["Least.U.TXT"].data.materials[0] = axis_label_colour
bpy.data.objects["Most.U.TXT"].data.materials[0] = axis_label_colour
bpy.data.objects["No.Data.TXT"].data.materials[0] = axis_label_colour
bpy.data.objects["Uncertainty.TXT"].data.materials[0] = axis_label_colour
bpy.data.objects["KeyTitle.TXT"].data.materials[0] = axis_label_colour

key_label = j_data["key_name"]
key_type = j_data["key_type"]
key_low = j_data["key_values"]["low_value"]
key_high = j_data["key_values"]["high_value"]
value_key_label = j_data["value_key_label"]

key_low = key_low.replace(' ', '\n')
key_high = key_high.replace(' ', '\n')

bpy.data.objects["Uncertainty.TXT"].data.body = key_label
bpy.data.objects["Least.U.TXT"].data.body = key_low
bpy.data.objects["Most.U.TXT"].data.body = key_high
bpy.data.objects["KeyTitle.TXT"].data.body = value_key_label

# ---------------------------------------------------------------

min_risk = None
max_risk = None

for idx in range(0, len(values)) :    
    datavalues = values[idx]
        
    lon = float(datavalues["x"])
    lat = float(datavalues["y"])    
    
    if background == "map":
        E, N = WGS84toOSGB36(lat, lon)

        d_x = (E + E_adj)
        d_y = (N + N_adj)
        
        if d_x > 500 or d_x < -500 or d_y > 500 or d_y < -500:
            #not on tile, ignore
            continue
    else:
        d_x = lon
        d_y = lat
    
    if (min_x == None or d_x < min_x):
        min_x = d_x
    if (max_x == None or d_x > max_x):
        max_x = d_x
    
    if (min_y == None or d_y < min_y):
        min_y = d_y
    if (max_y == None or d_y > max_y):
        max_y = d_y
    
    if 'r' in datavalues:
        d_r = float(datavalues["r"])
        if (min_risk == None or min_risk > d_r):
            min_risk = d_r
        if (max_risk == None or max_risk < d_r):
            max_risk = d_r

#------------------------------------------------------------------------------------------------------------------- RENDER

bpy.context.window.scene = bpy.data.scenes['Overlay']

if background == "graph":
    x_inc = (max_x - min_x)/10.0
    y_inc = (max_y - min_y)/8.0

    drawXAxis(min_x, max_x, x_inc, j_data["x_axis_label"])
    drawYAxis(min_y, max_y, y_inc, j_data["y_axis_label"])

drawKey(0.0, key_type, ortho, axis_value_colour)

if background == "map":
    bpy.context.window.scene = bpy.data.scenes['Scene']
    
    cam_offset = ((max_x - min_x) / 3.0)
    cam_offset = max(0.2, cam_offset)

    cam_x = ((min_x + max_x) / 2.0) + cam_offset
    cam_y = (min_y + max_y) / 2.0

    cam_orth_scale_x = (max_x - min_x) * 1.1
    cam_orth_scale_y = (max_y - min_y) * 1.1

    cam_orth_scale = max(cam_orth_scale_x, cam_orth_scale_y) * 2.0
    cam_orth_scale = max(cam_orth_scale, 1.5)

    camera = bpy.context.scene.objects["Camera"]
    camera.location = (cam_x, cam_y, 500)
    camera.data.ortho_scale = cam_orth_scale

for idx in range(0, len(values)) :    
    datavalues = values[idx]
    
    lon = float(datavalues["x"])
    lat = float(datavalues["y"])    
    
    if background == "map":
        E, N = WGS84toOSGB36(lat, lon)

        d_x = (E + E_adj)
        d_y = (N + N_adj)
        
        if d_x > 500 or d_x < -500 or d_y > 500 or d_y < -500:
            #print("glyph not on tile")     #not on tile, ignore
            continue
    else:
        d_x = start_x + ((lon - x_axis_values[0]) * (x_axis_length / (x_axis_values[len(x_axis_values)-1] - x_axis_values[0])))
        d_y = start_y + ((lat - y_axis_values[0]) * (y_axis_length / (y_axis_values[len(y_axis_values)-1] - y_axis_values[0])))
    
    d_uncertainty = float(datavalues["u"])
    d_value = float(datavalues["v"])
    
    if (key_type == "covid19"):         #bodge for covid-19 data
        if (d_uncertainty > 600):       #TODO automatically calculate uncertainty from range ...
            d_uncertainty = 0.56        # ... and/or give user option to specifiy uncertainty ranges
        elif (d_uncertainty > 600):
            d_uncertainty = 0.42
        elif (d_uncertainty > 400):
            d_uncertainty = 0.28
        elif (d_uncertainty > 200):
            d_uncertainty = 0.14
        elif (d_uncertainty > 0):
            d_uncertainty = 0.0
    
    if 'r' in datavalues:
        d_risk = float(datavalues["r"])
        risk_range = max_risk - min_risk
    
        if (risk_range <= 0):
            risk_val = d_risk
        else:
            risk_val = (d_risk - min_risk) / risk_range
    else:
        risk_val = 0.5      #print ("> No risk data")
    
    if background == "map":
        #glyph_scale = (cam_orth_scale / 1.5) * 0.25    
        glyph_size = 10.0 * glyph_scale
        scale = glyph_size + (risk_val * glyph_size)
        force = False
        height = 100.0
    else:
        glyph_size = 0.5 * glyph_scale
        scale = glyph_size + (risk_val * glyph_size)
        force = True
        height = 1.0
    
    pos = (d_x, d_y, height)
    name = "data-glyph-"+str(idx)
    glyphMat = getGlyphMaterial(d_value, key_type)
    glyph = initGlyph(d_uncertainty, 1, pos, scale, d_value, glyphMat, name, force) 
    createGlyph( glyph, minVariance, maxVariance, ortho, numGlyphs )

#bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)