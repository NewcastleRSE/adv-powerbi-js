import bpy

class Material:
    def make_material(self, name):
        self.mat = bpy.data.materials.new(name)
        self.mat.use_nodes = True
        self.nodes = self.mat.node_tree.nodes

    def link(self, from_node, from_slot_name, to_node, to_slot_name):
        input = to_node.inputs[to_slot_name]
        output = from_node.outputs[from_slot_name]
        self.mat.node_tree.links.new(input, output)

    def makeNode(self, type, name):
        self.node = self.nodes.new(type)
        self.node.name = name
        self.xpos += 200
        self.node.location = self.xpos, self.ypos
        return self.node

    def dump_node(self, node):
        node = node

    def new_row():
        self.xpos = 0
        self.ypos += 200

    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        
def makeFlatColor(flatColour, flatName):
    m = Material()
    
    thisMat = m.make_material(flatName)
    for n in m.nodes:
        m.nodes.remove(n)

    lightPath = m.makeNode('ShaderNodeLightPath', 'LightPath')

    transparentBSDF = m.makeNode(
        'ShaderNodeBsdfTransparent', 'Transparent BSDF')
    transparentBSDF.inputs["Color"].default_value = [1.0, 1.0, 1.0, 0.0]

    emissionBSDF = m.makeNode('ShaderNodeEmission', 'Emission')
    emissionBSDF.inputs["Color"].default_value = flatColour

    mixShader = m.makeNode('ShaderNodeMixShader', 'Mix Shader')
    m.dump_node(mixShader)

    materialOutput = m.makeNode('ShaderNodeOutputMaterial', 'Material Output')

    mixShader.inputs['Fac'].default_value = 0.3
    m.link(lightPath, 'Is Camera Ray', mixShader, 0)
    m.link(transparentBSDF, 'BSDF', mixShader, 1)
    m.link(emissionBSDF, 'Emission', mixShader, 2)
    m.link(mixShader, 'Shader', materialOutput, 'Surface')

    return thisMat

def makePrincipled(principledColor, principledName):
    m = Material()
    
    thisMat = m.make_material(principledName)
    for n in m.nodes:
        m.nodes.remove(n)

    principledBSDF = m.makeNode(
        'ShaderNodeBsdfPrincipled', 'Principled BSDF')
    principledBSDF.inputs["Base Color"].default_value = principledColor
    principledBSDF.inputs["Specular"].default_value = 0.1

    materialOutput = m.makeNode(
        'ShaderNodeOutputMaterial', 'Material Output')

    m.link(principledBSDF, 'BSDF', materialOutput, 'Surface')

    return thisMat

def makeEmissive(emissiveColour, emissiveName):
    m = Material()
    
    thisMat = m.make_material(emissiveName)
    for n in m.nodes:
        m.nodes.remove(n)
        
    emission = m.makeNode('ShaderNodeEmission', 'Emission')
    emission.inputs["Color"].default_value = emissiveColour
    emission.inputs["Strength"].default_value = 1.0
    
    materialOutput = m.makeNode('ShaderNodeOutputMaterial', 'Material Output')
    m.link(emission, 'Emission', materialOutput, 'Surface')
    
    return thisMat
    
def makeEmissiveAlpha(emissiveColour, emissiveName):
    m = Material()
    
    thisMat = m.make_material(emissiveName)
    for n in m.nodes:
        m.nodes.remove(n)
       
    transparentBSDF = m.makeNode(
        'ShaderNodeBsdfTransparent', 'Transparent BSDF')
    transparentBSDF.inputs["Color"].default_value = [1.0, 1.0, 1.0, 1.0]
    
    emission = m.makeNode('ShaderNodeEmission', 'Emission')
    emission.inputs["Color"].default_value = emissiveColour
    emission.inputs["Strength"].default_value = 1.0
        
    mixShader = m.makeNode('ShaderNodeMixShader', 'Mix Shader')
    
    mixShader.inputs['Fac'].default_value = emissiveColour[3]
    m.link(transparentBSDF, 'BSDF', mixShader, 1)
    m.link(emission, 'Emission', mixShader, 2)
    
    materialOutput = m.makeNode('ShaderNodeOutputMaterial', 'Material Output')
    m.link(mixShader, 'Shader', materialOutput, 'Surface')
    
    return thisMat

#
#  Function to set an objects material
#
def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)