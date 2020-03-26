import bpy

from Material import makeFlatColor

#
# Make some materials to use.
#
Mwhite = makeFlatColor((1.0, 1.0, 1.0, 1.0), 'ValWhite')
Mwhite = bpy.data.materials['ValWhite']
Mgrey = makeFlatColor((0.2, 0.2, 0.2, 1.0), 'ValGrey')
Mgrey = bpy.data.materials['ValGrey']
Mblack = makeFlatColor((0.0, 0.0, 0.0, 1.0), 'ValBlack')
Mblack = bpy.data.materials['ValBlack']

Myellow = makeFlatColor((0.9921568627450981, 0.8, 0.3843137254901961, 1.0), 'ValYellow')
Myellow = bpy.data.materials['ValYellow']