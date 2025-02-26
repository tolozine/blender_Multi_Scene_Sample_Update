import bpy

bl_info = {
    "name": "Batch Update Samples",
    "blender": (2, 80, 0),
    "category": "Render",
    "author": "tolozine",
    "version": (1, 5),
    "description": "Batch modify max samples and noise threshold for all scenes",
}

class RENDER_PT_BatchUpdateSamples(bpy.types.Panel):
    bl_label = "采样批量修改"
    bl_idname = "RENDER_PT_batch_update_samples"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "采样批量修改"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "batch_max_samples")
        layout.prop(scene, "batch_min_samples")
        layout.prop(scene, "batch_noise_threshold")
        layout.operator("render.batch_update_samples")

class RENDER_OT_BatchUpdateSamples(bpy.types.Operator):
    bl_label = "应用到所有场景"
    bl_idname = "render.batch_update_samples"
    bl_description = "Apply max samples, min samples, and noise threshold to all scenes"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        max_samples = context.scene.batch_max_samples
        min_samples = context.scene.batch_min_samples
        noise_threshold = context.scene.batch_noise_threshold

        for scene in bpy.data.scenes:
            if scene.render.engine == 'CYCLES':
                scene.cycles.samples = max_samples
                scene.cycles.use_adaptive_sampling = True
                scene.cycles.adaptive_threshold = noise_threshold
                scene.cycles.adaptive_min_samples = min_samples

        self.report({'INFO'}, "采样值、最小采样数和阈值已更新")
        return {'FINISHED'}

def register():
    bpy.utils.register_class(RENDER_PT_BatchUpdateSamples)
    bpy.utils.register_class(RENDER_OT_BatchUpdateSamples)
    bpy.types.Scene.batch_max_samples = bpy.props.IntProperty(
        name="最大采样数", default=1024, min=1)
    bpy.types.Scene.batch_min_samples = bpy.props.IntProperty(
        name="最小采样数", default=32, min=1)
    bpy.types.Scene.batch_noise_threshold = bpy.props.FloatProperty(
        name="噪点阈值", default=0.01, min=0.0, max=1.0)

def unregister():
    bpy.utils.unregister_class(RENDER_PT_BatchUpdateSamples)
    bpy.utils.unregister_class(RENDER_OT_BatchUpdateSamples)
    del bpy.types.Scene.batch_max_samples
    del bpy.types.Scene.batch_min_samples
    del bpy.types.Scene.batch_noise_threshold

if __name__ == "__main__":
    register()
