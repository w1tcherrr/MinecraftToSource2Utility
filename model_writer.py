import os


def traverse_and_generate_models(directory: str):
    for root, dirs, files in os.walk(directory):
        for subdir in dirs:
            subdir_path = os.path.join(root, subdir)
            parent_dir = os.path.dirname(subdir_path)
            output_file = os.path.join(parent_dir, f"detail_model_{subdir}.vmdl")
            generate_modeldoc(subdir_path, output_file)


def generate_modeldoc(directory: str, output_file: str):
    if not os.path.isdir(directory):
        raise ValueError(f"The directory {directory} does not exist.")

    fbx_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.fbx'):
                full_path = os.path.join(root, file)
                relative_path = full_path.split("csgo_addons", 1)[1]
                relative_path = relative_path.split("\\", 1)[1]
                relative_path = relative_path.lstrip("/\\")
                relative_path = relative_path.split("\\", 1)
                relative_path = relative_path[1]
                fbx_files.append(relative_path.lstrip('/\\'))

    if not fbx_files:
        raise ValueError(f"No .fbx files found in the directory {directory}.")

    base_structure = """
    {{
        rootNode = 
        {{
            _class = "RootNode"
            children = 
            [
                {{
                    _class = "RenderMeshList"
                    children = 
                    [
                        {RENDER_MESH_FILES}
                    ]
                }}
            ]
            model_archetype = ""
            primary_associated_entity = ""
            anim_graph_name = ""
            document_sub_type = "ModelDocSubType_None"
        }}
    }}
    """

    render_mesh_file_template = """
                    {{
                        _class = "RenderMeshFile"
                        filename = "{filename}"
                        import_scale = 1.0
                        import_filter = 
                        {{
                            exclude_by_default = false
                            exception_list = [  ]
                        }}
                    }}
    """

    render_mesh_files = ""
    for fbx_file in fbx_files:
        render_mesh_files += render_mesh_file_template.format(filename=f'{fbx_file.replace("\\", "/")}') + ","

    render_mesh_files = render_mesh_files.rstrip(',')

    final_structure = base_structure.replace("{RENDER_MESH_FILES}", render_mesh_files)

    with open(output_file, 'w') as f:
        f.write(
            "<!-- kv3 encoding:text:version{e21c7f3c-8a33-41c5-9977-a76d3a32aa0d} format:modeldoc36:version{972dada4-b828-45a4-bb93-7795cf0585da} -->\n")
        f.write(final_structure.replace("{{", "{").replace("}}", "}"))
