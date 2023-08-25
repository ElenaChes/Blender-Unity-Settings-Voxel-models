bl_info = {
    "name" : "Unity Settings",
    "author" : "Len",
    "version" : (1, 1),
    "blender" : (3, 2, 1),
    "location" : "View3d > Sidebar/N-Panel > Unity Settings",
    "description": "Process MagicaVoxel models for Unity.",
    "warning" : "Dependencies: [VoxCleaner v1 by Farhan Shaikh] and [Texel Density Checker v3.3.1 by Ivan Vostrikov]",
    "category" : "Game Engine",
}

import os
import bpy
from bpy.props import (StringProperty, EnumProperty, BoolProperty)  

#-------------Properties------------   
def saveScale(self, context):
    utool = context.scene.unity_tool
    check = 10.0 
    try:
        check = float(utool.uScale)
    except:
        check = 0.001
        utool['uScale'] = '0.001'  
        
    if check < 0.01:
        check = 10.0
        utool['uScale'] = '10.0' 

def saveModelSize(self, context):
    utool = context.scene.unity_tool
    check = 256 
    if utool.uModelSize == 'cstm':
        try:
            check = int(utool.uCustomSize)
        except:
            check = 256
            utool['uCustomSize'] = '256'
    else:   
        check = int(utool.uModelSize) 
        utool['uCustomSize'] = utool.uModelSize 
        
    if check < 8 or check > 1024:
        check = 256
        utool['uCustomSize'] = '256'
            
def saveMargin(self, context):
    utool = context.scene.unity_tool
    check = 0.001 
    try:
        check = float(utool.uMargin)
    except:
        check = 0.001
        utool['uMargin'] = '0.001'  
        
    if check < 0 or check > 1:
        check = 0.001
        utool['uMargin'] = '0.001'  

def saveTD(self, context):
    utool = context.scene.unity_tool
    check = 0.1 
    try:
        check = float(utool.uTD)
    except:
        check = 0.1
        utool['uTD'] = '0.1'  
        
    if check < 0.001 or check > 1:
        check = 0.1
        utool['uTD'] = '0.1'  
        
def saveDecimate(self, context):
    utool = context.scene.unity_tool
    check = 0.1 
    try:
        check = float(utool.uDecimate)
    except:
        check = 0.5
        utool['uDecimate'] = '0.5'  
        
    if check < 0 or check > 1:
        check = 0.5
        utool['uDecimate'] = '0.5'                

class uProperties(bpy.types.PropertyGroup):
    uName : StringProperty(
        name="",
        description="File's name",
        default="") 
    uTexName : StringProperty(
        name="",
        description="File's name",
        default="") 
    uSmart : BoolProperty(
        name="",
        description="USe smart process?",
        default=True) 
#   [Model state]    
    uStep : StringProperty(
        name="",
        description="Current step",
        default="0")
    uProcessed : BoolProperty(
        name="",
        description="Model ready",
        default=False)
    uLOD : BoolProperty(
        name="",
        description="Low LOD model ready",
        default=False)    
    uTexture : BoolProperty(
        name="",
        description="Texture ready",
        default=False)
#   [Model size]
    uModelSize : EnumProperty(name="Model",
        items = 
        [("256", "Regular (256x256)", ""),
        ("1024", "Prop (1024x1024)", ""),
        ("cstm", "Custom", "")],
        update = saveModelSize)
    uCustomSize : StringProperty(
        name="",
        description="Custom Resolution",
        default="256",
        update = saveModelSize)
#   [UV Settings]
    uMargin : StringProperty(
        name="",
        description="Margin for UV",
        default="0.001",
        update = saveMargin)
    uTD: StringProperty(
        name="",
        description="TD for Texel",
        default="0.1",
        update = saveTD)
#   [LOD Settings]
    uDecimate : StringProperty(
        name="",
        description="Ratio for Decimate",
        default="0.5",
        update = saveDecimate)
#   [Export]
    uFlipZ: BoolProperty(
        name="",
        description="Should export flip Z axis?",
        default=True)
    uScale : StringProperty(
        name="",
        description="Margin for UV",
        default="10.0",
        update = saveScale) 
    uAutoExport : BoolProperty(
        name="",
        description="Should auto export files?",
        default=True)        
    uModelPath : StringProperty(
        name="",
        description="Path to save obj files",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')
    uTexturePath : StringProperty(
        name="",
        description="Path to save texture",
        default="",
        maxlen=1024,
        subtype='DIR_PATH')             

#------------UI functions-----------   
class uSettingsPanel(bpy.types.Panel):
    bl_label = "Model Settings"
    bl_idname = "UNITY_PT_uSettings_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Unity Settings'
    
    def draw(self, context):
        layout = self.layout
        utool = context.scene.unity_tool
#   [Model Size]
        box = layout.box()
        box.label(text="Model Size", icon="MODIFIER_OFF")
        row = box.row()#new row
        row.prop(utool, "uModelSize")
        if utool.uModelSize == 'cstm':
            row = box.row()#new row
            row.label(text="Custom:")
            row.prop(utool, "uCustomSize")
            row.label(text=f"x {utool.uCustomSize}")
#   [UV Settings]        
        box = layout.box()
        box.label(text="UI Settings", icon="TEXTURE_DATA")
        row = box.row()#new row
        row.label(text="Island Margin:")
        row.prop(utool, "uMargin")
        row = box.row()#new row
        row.label(text="Set TD:")
        row.prop(utool, "uTD")
        row.label(text="px/cm")
#   [Quick Start]  
        box = layout.box()
        box.label(text="Quick Start", icon="SORTTIME")
        row = box.row()#new row 
        if utool.uProcessed or utool.uLOD or not utool.uStep == '0':
            row.operator("usettings.confirm", text="New Model", icon="OUTLINER_OB_LIGHT") 
        else:
            row.operator("usettings.importobj", text="New Model", icon="OUTLINER_OB_LIGHT") 

class uExportPanel(bpy.types.Panel):
    bl_label = "Quick Export"
    bl_idname = "UNITY_PT_uExport_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Unity Settings'
    
    def draw(self, context):
        layout = self.layout
        utool = context.scene.unity_tool

        box = layout.box()
        row = box.row()#new row
        row.label(text="Auto Export:")
        row.prop(utool, "uAutoExport")
#   [Texture Export]
        box = layout.box()
        box.label(text="Texture", icon="VIEW_ORTHO")
        row = box.row()#new row
        if utool.uAutoExport:
            row.label(text="Texture Path:")
            row.prop(utool, "uTexturePath")
        else:    
            if utool.uTexture:
                row.operator("usettings.export_texture", text="Export", icon="FILEBROWSER") 
            else:
                row.label(text="Process model first", icon="BORDERMOVE")  
#   [Obj Export]       
        box = layout.box()
        if utool.uLOD:
            box.label(text="Low LOD Obj", icon="FILE_3D")    
        else:
            box.label(text="Obj", icon="FILE_3D")
        row = box.row()#new row
        row.label(text="Flip Z axis:")
        row.prop(utool, "uFlipZ")
        row = box.row()#new row
        row.label(text="Scale:")
        row.prop(utool, "uScale")
        row = box.row()#new row
        if utool.uAutoExport:
            row.label(text="Model Path:")
            row.prop(utool, "uModelPath")
        else:    
            if len(bpy.context.selected_objects) == 1:
                if bpy.context.active_object == bpy.context.selected_objects[0]:
                    if utool.uProcessed:
                        row.operator("usettings.export_obj", text="Export", icon="FILEBROWSER") 
                    else:
                        row.label(text="Process model first", icon="BORDERMOVE")  
                else:
                    row.label(text="Select a model", icon="BORDERMOVE")  
            else:
                row.label(text="Select a model", icon="BORDERMOVE")                               

class uProcessPanel(bpy.types.Panel):
    bl_label = "Process Model"
    bl_idname = "UNITY_PT_uProcess_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Unity Settings'
    
    def draw(self, context):
        layout = self.layout
        utool = context.scene.unity_tool
        box = layout.box()
        row = box.row()#new row   
        row.label(text="Use smart process:")
        row.prop(utool, "uSmart")
        box = layout.box()
        if utool.uSmart:
            if utool.uLOD:
                box.label(text="LOD Processed", icon="CHECKMARK") 
            elif utool.uProcessed:
                box.label(text="Processed", icon="CHECKMARK") 
            else:
                box.label(text="Not Processed", icon="X")   
        else: 
            if utool.uLOD:
                box.label(text="Steps complete: 8/7", icon="MENU_PANEL") 
            elif utool.uProcessed:
                box.label(text="Steps complete: 7/7", icon="MENU_PANEL") 
            elif utool.uTexture:
                box.label(text="Steps complete: 6/7", icon="MENU_PANEL") 
            else:
                box.label(text=f"Steps complete: {utool.uStep}/7", icon="MENU_PANEL") 
        row = box.row()#new row
        if len(bpy.context.selected_objects) == 1:
            if bpy.context.active_object == bpy.context.selected_objects[0]:
        #   [Run smart process] 
                if utool.uSmart:
                    row.operator("usettings.smart_process", text="Smart Process", icon="BRUSH_DATA") 
                else:
        #   [Run process step by step] 
                    row.operator("usettings.start_process", text="Start Process", icon="OBJECT_HIDDEN")  
                    row = box.row()#new row
                    row.operator("usettings.prepare_uv", text="Prepare For UV", icon="SHADERFX")  
                    row = box.row()#new row
                    row.operator("usettings.pack_islands", text="Pack Islands", icon="UV_EDGESEL")  
                    row = box.row()#new row
                    row.operator("usettings.update_td", text="Update TD", icon="GROUP_VERTEX")  
                    row = box.row()#new row
                    row.operator("usettings.set_pixels", text="Set To Pixels", icon="TEXTURE_DATA")  
                    row = box.row()#new row
                    row.operator("usettings.bake_texture", text="Bake Texture", icon="UV") 
                    row = box.row()#new row
                    row.operator("usettings.pretty_polygons", text="Pretty Polygons", icon="MOD_WIREFRAME") 
            else:
                row.label(text="Select a model", icon="BORDERMOVE")  
        else:
            row.label(text="Select a model", icon="BORDERMOVE")              

class uLODPanel(bpy.types.Panel):
    bl_label = "Level Of Detail"
    bl_idname = "UNITY_PT_uLOD_Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Unity Settings'

    def draw(self, context):
        layout = self.layout
        utool = context.scene.unity_tool
        box = layout.box()    
        if utool.uLOD:
            box.label(text="LOD Processed", icon="CHECKMARK") 
        else:
            box.label(text="LOD Not Processed", icon="X") 
        row = box.row()#new row
        row.label(text="Decimate:")
        row.prop(utool, "uDecimate")
        row = box.row()#new row
        if len(bpy.context.selected_objects) == 1:
            if bpy.context.active_object == bpy.context.selected_objects[0]:
        #   [LOD Settings]  
                if utool.uProcessed or utool.uLOD:
                    row.operator("usettings.lod", text="Process", icon="CAMERA_STEREO")  
                else:
                    row.label(text="Process model first", icon="BORDERMOVE")  
            else:
                row.label(text="Select a model", icon="BORDERMOVE")  
        else:
            row.label(text="Select a model", icon="BORDERMOVE")   

#----------Button functions---------  
class Confirm_Operator(bpy.types.Operator):
    """Quick obj import button"""
    bl_idname = "usettings.confirm"
    bl_label = "Wait! Did you export the current model?"
    bl_options = {'REGISTER', 'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.usettings.importobj()
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

class Import(bpy.types.Operator):
    """Quick obj import button"""
    bl_idname = "usettings.importobj"
    bl_label = "New Model"
    bl_options = {'UNDO'}

    def execute(self, context):
        if bpy.context.active_object:
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        delExtras(self, context, True)
        bpy.ops.import_scene.obj('INVOKE_DEFAULT')
        utool = context.scene.unity_tool
        utool.uStep = '0'
        utool.uTexture = False
        utool.uProcessed = False
        utool.uLOD = False
        bpy.context.space_data.shading.type = 'SOLID'
        bpy.context.space_data.overlay.show_wireframes = False
        return {'FINISHED'}

class Smart_Process(bpy.types.Operator):
    """Run: 
-prepare for UV,
-cube projections,
-pack islands,
-set TD,
-selected to pixels
-bake texture,
-traingulate,
-tris to quads"""
    bl_idname = "usettings.smart_process"
    bl_label = "Smart Process"
    bl_options = {'UNDO'}

    def execute(self, context):
        if StartProcess(self, context):
            return {'CANCELLED'} 
#   [Prepare for UV]
        if PrepareForUV(self, context):
            return {'CANCELLED'} 
        context = bpy.context
#   [Pack Islands]
        if CubeIslands(self, context):
            return {'CANCELLED'} 
#   [Update TD]   
        if UpdateTD(self, context):
            return {'CANCELLED'} 
#   [Set Pixels]  
        if SetToPixels(self, context):
            return {'CANCELLED'} 
#   [Bake]
        if Texture(self, context):
            return {'CANCELLED'} 
#   [Process polygons]
        if Polygons(self, context):
            return {'CANCELLED'}
        utool = context.scene.unity_tool
        if utool.uAutoExport:
            auto(self, context, True) 
        else:     
            bpy.context.window_manager.popup_menu(smart, title="", icon='INFO')     
        return {'FINISHED'} 
          
class Start_Process(bpy.types.Operator):
    """Removes all objects except selected"""
    bl_idname = "usettings.start_process"
    bl_label = "Select Model"
    bl_options = {'UNDO'}
    
    #Used to do what Import() does now (resetting variables and deleting extra objects), 
    #but removing it completely from the process was too much work  
    def execute(self, context):
        if StartProcess(self, context):
            return {'CANCELLED'} 
        return {'FINISHED'} 

class Prepare_UV(bpy.types.Operator):
    """Runs: 
-prepare for UV"""
    bl_idname = "usettings.prepare_uv"
    bl_label = "Prepare for UV"
    bl_options = {'UNDO'}

    def execute(self, context):
        if PrepareForUV(self, context):
            return {'CANCELLED'} 
        return {'FINISHED'} 

class Pack_Islands(bpy.types.Operator):
    """Runs: 
-cube projections,
-pack islands"""
    bl_idname = "usettings.pack_islands"
    bl_label = "Pack Islands"
    bl_options = {'UNDO'}

    def execute(self, context):
        if CubeIslands(self, context):
            return {'CANCELLED'} 
        return {'FINISHED'} 

class Update_TD(bpy.types.Operator):
    """Runs: 
-selected to pixels"""
    bl_idname = "usettings.update_td"
    bl_label = "Update TD"
    bl_options = {'UNDO'}

    def execute(self, context):
        if UpdateTD(self, context):
            return {'CANCELLED'} 
        return {'FINISHED'}  
    
class Set_Pixels(bpy.types.Operator):
    """Runs: 
-selected to pixels"""
    bl_idname = "usettings.set_pixels"
    bl_label = "Set To Pixels"
    bl_options = {'UNDO'}

    def execute(self, context):
        if SetToPixels(self, context):
            return {'CANCELLED'} 
        return {'FINISHED'}               

class Bake_Texture(bpy.types.Operator):
    """Runs: 
-bake texture"""
    bl_idname = "usettings.bake_texture"
    bl_label = "Bake Texture"
    bl_options = {'UNDO'}

    def execute(self, context):
        if Texture(self, context):
            return {'CANCELLED'} 
        bpy.context.window_manager.popup_menu(texture, title="", icon='INFO')
        return {'FINISHED'}      
    
class Pretty_Polygons(bpy.types.Operator):
    """Runs: 
-traingulate
-tris to quads"""
    bl_idname = "usettings.pretty_polygons"
    bl_label = "Pretty Polygons"
    bl_options = {'UNDO'}

    def execute(self, context):
        if Polygons(self, context):
            return {'CANCELLED'} 
        bpy.context.window_manager.popup_menu(obj, title="", icon='INFO')
        return {'FINISHED'}   
    
class LOD_Version(bpy.types.Operator):
    """Runs: 
-decimate"""
    bl_idname = "usettings.lod"
    bl_label = "LOD Version"
    bl_options = {'UNDO'}

    def execute(self, context):
        if LOD(self, context):
            return {'CANCELLED'}  
        utool = context.scene.unity_tool 
        if utool.uAutoExport:
            auto(self, context, False) 
        else:
            bpy.context.window_manager.popup_menu(lod, title="", icon='INFO') 
        return {'FINISHED'}   
    
class Export_Texture(bpy.types.Operator):
    """Opens export texture window"""
    bl_idname = "usettings.export_texture"
    bl_label = "Export Texture"
    bl_options = {'UNDO'}

    def execute(self, context):   
        area = bpy.context.area
        old_type = area.ui_type
        area.ui_type = 'UV'
        try:
            bpy.ops.image.save_as('INVOKE_DEFAULT')
        except:
            self.report({'ERROR'}, "Failed to prompt export")
        area.ui_type = old_type
        return {'FINISHED'} 

class Export_Obj(bpy.types.Operator):
    """Opens export obj window with correct settings"""
    bl_idname = "usettings.export_obj"
    bl_label = "Export Obj"
    bl_options = {'UNDO'}

    def execute(self, context):
        try:
            utool = context.scene.unity_tool
            scale = float(utool.uScale)
            zState = 'Z'
            if not utool.uFlipZ:
                zState ='-Z' 
            if not utool.uAutoExport:     
                bpy.ops.export_scene.obj('INVOKE_DEFAULT', use_selection=True, global_scale=scale, axis_forward=zState) 
            else:
                path = os.path.join(utool.uModelPath, utool.uName + "_LOD.obj")    
                bpy.ops.export_scene.obj('INVOKE_DEFAULT', filepath=path, use_selection=True, global_scale=scale, axis_forward=zState)
        except:
            self.report({'ERROR'}, "Failed to prompt export")
        return {'FINISHED'}       

#----------Category functions---------
def StartProcess(self, context):
    utool = context.scene.unity_tool
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    selected = bpy.context.selected_objects
    #Used to do what Import() does now (resetting variables and deleting extra objects), 
    #but removing it completely from the process was too much work
    if not len(selected) == 1:
        self.report({'ERROR'}, "Clearing failed, couldn't select model")
        return True #fail
    if not bpy.context.active_object == selected[0]:
        self.report({'ERROR'}, "Clearing failed, couldn't select model")
        return True #fail
    bpy.context.space_data.overlay.show_wireframes = True
    bpy.context.space_data.shading.type = "MATERIAL"    
    self.report({'INFO'}, "Selected model and ready for processing")
    utool.uStep = '1'
    return False    #success
       
def PrepareForUV(self, context):
    utool = context.scene.unity_tool
    if not utool.uStep == '1':
        self.report({'WARNING'}, "UV cancelled, select model first")
        return True #fail    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
#   [Prepare For UV]        
    utool.uName = bpy.context.active_object.name
    vox = bpy.context.scene.my_tool
    vox.ResX = int(utool.uCustomSize)
    vox.ResY = int(utool.uCustomSize)
    bpy.ops.voxcleaner.prepareforuv()
    utool.uTexName = bpy.context.active_object.name + "Tex"
    model = bpy.context.active_object  
    model.name = utool.uName
    self.report({'INFO'}, "Prepared for UV")
    utool.uStep = '2'
    return False    #success  

def CubeIslands(self, context):
    utool = context.scene.unity_tool
    if not utool.uStep == '2':
        self.report({'WARNING'}, "Islands cancelled, prepare for UV first")
        return True #fail    
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
#   [Pack Islands]        
    bpy.ops.uv.cube_project()
    bpy.ops.uv.select_all(action='SELECT')
    bpy.ops.uv.pack_islands(rotate=False, margin=float(utool.uMargin))
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    self.report({'INFO'}, "Cube islands packed")
    utool.uStep = '3'
    return False    #success   
   
def UpdateTD(self, context):
    utool = context.scene.unity_tool
    if not utool.uStep == '3':
        self.report({'WARNING'}, "TD cancelled, pack islands first")
        return True #fail    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
#   [Update TD]
    texel = bpy.context.scene.td
    texel.texture_size = '4'
    texel.custom_width = utool.uCustomSize
    texel.custom_height = utool.uCustomSize
    texel.density_set = utool.uTD
    bpy.ops.object.texel_density_set()
    self.report({'INFO'}, "TD updated")
    utool.uStep = '4'
    return False    #success  

def SetToPixels(self,context):
    utool = context.scene.unity_tool
    if not utool.uStep == '4':
        self.report({'WARNING'}, "Setting to pixels cancelled, set TD first") 
        return True #fail  
#   [Set To Pixels]
    area = bpy.context.area
    old_type = area.ui_type
    area.ui_type = 'UV'
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.context.area.spaces.active.image = bpy.data.images[utool.uTexName] 
    bpy.ops.uv.snap_selected(target='PIXELS')
    area.ui_type = old_type
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    self.report({'INFO'}, "Set to pixels")
    utool.uStep = '5'
    return False    #success  

def Texture(self, context):   
    utool = context.scene.unity_tool
    if not utool.uStep == '5':
        self.report({'WARNING'}, "Baking cancelled, set to pixels first")   
        return True #fail    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False) 
#   [Bake Texture]
    bpy.ops.voxcleaner.postuvbake()
    for mat in bpy.data.materials:
        if not mat.node_tree:
            continue
        for node in mat.node_tree.nodes:
            if node.type == 'TEX_IMAGE':
                node.interpolation = 'Closest'
    if delExtras(self, context, False):
        self.report({'ERROR'}, "Bakin texture failed, accidentally deleted model")
        return True #fail        
    self.report({'INFO'}, "Baked texture")
    utool.uTexture = True
    return False    #success  
       
def Polygons(self, context):
    utool = context.scene.unity_tool
    if not utool.uTexture:
        self.report({'WARNING'}, "Polygon processing cancelled, bake first")   
        return True #fail    
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
#   [Edit Polygons]    
    bpy.ops.object.modifier_add(type='TRIANGULATE')
    bpy.context.object.modifiers["Triangulate"].quad_method = 'BEAUTY'
    bpy.ops.object.modifier_apply(modifier="Triangulate")
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.tris_convert_to_quads(face_threshold=3.14159, shape_threshold=3.14159, uvs=True)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    self.report({'INFO'}, "Edited polygons")
    utool.uStep = "0"
    utool.uProcessed = True
    return False    #success  

def LOD(self, context):
    utool = context.scene.unity_tool
    if not utool.uProcessed:
        self.report({'WARNING'}, "Low LOD cancelled, process model first")
        return True #fail
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
#   [Create LOD Version]  
    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].ratio = float(utool.uDecimate)
    bpy.ops.object.modifier_apply(modifier="Decimate")
    model = bpy.context.active_object  
    utool.uName = utool.uName + "_LOD"
    model.name = utool.uName
    self.report({'INFO'}, "Low LOD version created")
    utool.uLOD = True
    return False    #success

def delExtras(self, context, full):
    model = bpy.context.active_object  
    if full:
        model = "none"
    else:
        model.select_set(False) 
    objs = bpy.data.objects      
    for obj in objs:
        print(obj.name)
        if not obj == model:
            obj.hide_set(False)
            obj.select_set(True)
    bpy.ops.object.delete(use_global=False, confirm=False) 
    if not model:
        return True #fail
    if not full:    
        model.select_set(True)
    return False    #success
   
def auto(self, context, full):
    utool = context.scene.unity_tool
#   [Export Texture]  
    if full:
        area = bpy.context.area
        old_type = area.ui_type
        area.ui_type = 'UV'
        try:
            image = bpy.data.images[utool.uTexName]
            image.filepath_raw = os.path.join(utool.uTexturePath, utool.uTexName + '.png')
            image.file_format = 'PNG'
            image.save()
            self.report({'INFO'}, "Exported texture")
            utool.uTexture = True
        except:
            self.report({'ERROR'}, "Failed to export texture")
        area.ui_type = old_type
#   [Export Model]    
    scale = float(utool.uScale)
    zState = 'Z'
    if not utool.uFlipZ:
        zState ='-Z'
    try:
        path = os.path.join(utool.uModelPath, utool.uName + ".obj")    
        bpy.ops.export_scene.obj('INVOKE_DEFAULT', filepath=path, use_selection=True, global_scale=scale, axis_forward=zState)
    except:
        if utool.uLOD:
            self.report({'ERROR'}, "Failed to export LOD model")
        else:    
            self.report({'ERROR'}, "Failed to export model")

#--------------Pop ups-------------  
def smart(self, context):
    self.layout.label(text="Obj and Texture are ready for export!")

def texture(self, context):
    self.layout.label(text="Texture is ready for export!")

def obj(self, context):
    self.layout.label(text="Obj is ready for export!")

def lod(self, context):
    self.layout.label(text="Low LOD verision is ready for export!")     

classes = (
#   [Properties]
    uProperties,
   
#   [Buttons]
    Confirm_Operator,
    Import,
    Smart_Process,
    Start_Process,
    Prepare_UV,
    Pack_Islands,
    Update_TD,
    Set_Pixels,
    Bake_Texture,
    Pretty_Polygons,
    LOD_Version,
    Export_Texture,
    Export_Obj,

#   [Panels]
    uSettingsPanel,
    uExportPanel,
    uProcessPanel,
    uLODPanel,
)        
         
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.Scene.unity_tool = bpy.props.PointerProperty(type= uProperties)
     
def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.unity_tool
    
if __name__ == "__main__":
    register()