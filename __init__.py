from .blender_pydeps import PythonRequirements

import bpy

bl_info = {
    "name": "Random Word Maker",
    "description": "Add random words to your blender scene",
    "author": "Joe Button",
    "version": (1, 0, 0),
    "blender": (2, 91, 0),
    "wiki_url": "https://github.com/Joeboy/blender-addon-pydeps",
    "tracker_url": "https://github.com/Joeboy/blender-addon-pydeps/issues",
    "support": "COMMUNITY",
    "category": "3D View"
}

python_requirements = PythonRequirements(
    [
        ('wheel', __import__),
        ('pyyaml', lambda n: __import__('yaml')),
        ('random-word', lambda n: __import__('random_word')),
    ]
)


class RANDOMWORDS_OT_DrawWordOperator(bpy.types.Operator):
    bl_idname = "randomwords.drawwordoperator"
    bl_label = "Draw Random Word"
    bl_description = "Draw a random_word."
    bl_options = {"REGISTER"}

    def execute(self, context):
        from random_word import RandomWords
        r = RandomWords()
        word = r.get_random_word()
        bpy.ops.object.text_add()
        ob=bpy.context.object
        ob.data.body = word
        return {"FINISHED"}


class RANDOMWORDS_PT_DrawWordsPanel(bpy.types.Panel):
    bl_label = "Draw Random Words"
    bl_category = "Random Words"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Draw a random word")
        layout.operator(RANDOMWORDS_OT_DrawWordOperator.bl_idname)


classes = (RANDOMWORDS_OT_DrawWordOperator, RANDOMWORDS_PT_DrawWordsPanel)


class RANDOMWORDS_PT_DrawWordsWarningPanel(bpy.types.Panel):
    bl_label = "Warning"
    bl_category = "Random Words"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return not python_requirements.requirements_installed

    def draw(self, context):
        layout = self.layout

        lines = [f"Please install the missing dependencies for the \"{bl_info.get('name')}\" add-on.",
                 f"1. Open the preferences (Edit > Preferences > Add-ons).",
                 f"2. Search for the \"{bl_info.get('name')}\" add-on.",
                 f"3. Open the details section of the add-on.",
                 f"4. Click on the \"{RANDOMWORDS_OT_InstallRequirementsOperator.bl_label}\" button.",
                 f"   This will download and install the missing Python packages, if Blender has the required",
                 f"   permissions.",
                 f"If you're attempting to run the add-on from the text editor, you won't see the options described",
                 f"above. Please install the add-on properly through the preferences.",
                 f"1. Open the add-on preferences (Edit > Preferences > Add-ons).",
                 f"2. Press the \"Install\" button.",
                 f"3. Search for the add-on file.",
                 f"4. Confirm the selection by pressing the \"Install Add-on\" button in the file browser."]

        for line in lines:
            layout.label(text=line)


class RANDOMWORDS_OT_InstallRequirementsOperator(bpy.types.Operator):
    bl_idname = "randomwords.install_requirements"
    bl_label = "Install requirements"
    bl_description = (
        "Downloads and installs the required python packages for this add-on. "
        "Internet connection is required. Blender may have to be started with "
        "elevated permissions in order to install the package"
    )
    bl_options = {"REGISTER", "INTERNAL"}

    @classmethod
    def poll(self, context):
        # Deactivate when dependencies have been installed
        return not python_requirements.requirements_installed

    def execute(self, context):
        if not python_requirements.requirements_installed:
            python_requirements.install_requirements()
            # Since dependencies are now installed, we can register the main
            # panels, operators etc:
            for cls in classes:
                bpy.utils.register_class(cls)

        return {"FINISHED"}


class RANDOMWORDS_preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator(RANDOMWORDS_OT_InstallRequirementsOperator.bl_idname, icon="CONSOLE")


preference_classes = [
    RANDOMWORDS_PT_DrawWordsWarningPanel,
    RANDOMWORDS_OT_InstallRequirementsOperator,
    RANDOMWORDS_preferences
]


def register():
    # Register the classes for the preferences dialog:
    for cls in preference_classes:
        bpy.utils.register_class(cls)
    # If requirements are already installed, also register the main classes:
    if python_requirements.requirements_installed:
        for cls in classes:
            bpy.utils.register_class(cls)


def unregister():
    for cls in preference_classes:
        bpy.utils.unregister_class(cls)

    if python_requirements.requirements_installed:
        for cls in classes:
            bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()