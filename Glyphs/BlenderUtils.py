import bpy

#function to specify the active render layer.
#all objects created after this call will be placed on the specified layer

def setActiveRenderLayer(layer):
    for i in range(20):
        bpy.context.scene.layers[i] = False
    
    bpy.context.scene.layers[layer] = True
    
def setAllRenderLayersActive():
    for i in range(20):
        bpy.context.scene.layers[i] = True