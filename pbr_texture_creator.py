import os
import json
import shutil
from PIL import Image, ImageOps


class TextureSetFinder:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.texture_set_keys = set()  # Set to store unique keys

    def find_texture_sets(self):
        # Walk through all subdirectories and files in the input directory
        for subdir, _, files in os.walk(self.input_dir):
            for file in files:
                # Check if the file ends with '_set.json'
                if file.endswith('_set.json'):
                    file_path = os.path.join(subdir, file)
                    self._process_file(file_path, subdir)

        # Print all unique keys found in the 'minecraft:texture_set' objects
        print("Unique keys found in 'minecraft:texture_set':")
        for key in sorted(self.texture_set_keys):
            print(key)

    def _process_file(self, file_path, subdir):
        try:
            # Open and load the JSON file
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                if "minecraft:texture_set" in data:
                    texture_set = data["minecraft:texture_set"]
                    self.texture_set_keys.update(texture_set.keys())
                    self._create_vmat_file(file_path, texture_set, subdir)
        except json.JSONDecodeError:
            print(f'Error decoding JSON in file: {file_path}')
        except Exception as e:
            print(f'An error occurred while processing the file {file_path}: {e}')

    def _create_vmat_file(self, json_path, texture_set, subdir):
        # Extract the base name without _set.json
        base_name = os.path.basename(json_path).replace('_set.json', '')

        # Prepare a list to hold paths of all textures to copy
        textures_to_copy = []

        # Determine the color texture and generate the translucency map from it
        color_texture = texture_set.get("color", f"{base_name}")
        color_texture_path = self._complete_texture_path(subdir, color_texture)
        translucency_path = None

        if color_texture_path and os.path.exists(color_texture_path):
            textures_to_copy.append(color_texture_path)

            # Generate the translucency map only from the color texture
            translucency_path = self._generate_translucency_map(color_texture_path)
            if translucency_path:
                textures_to_copy.append(translucency_path)

        # Add other textures from the set, but do not generate additional translucency maps
        for key, texture in texture_set.items():
            if key != "color":  # Skip the color texture, already handled
                texture_path = self._complete_texture_path(subdir, texture)
                if texture_path and os.path.exists(texture_path):
                    textures_to_copy.append(texture_path)

        # Maintain the relative directory structure in the output
        relative_output_dir = os.path.relpath(subdir, self.input_dir)
        output_dir_path = os.path.join(self.output_dir, relative_output_dir)
        os.makedirs(output_dir_path, exist_ok=True)

        # Copy the texture files to the output directory
        self._copy_texture_files(textures_to_copy, output_dir_path)

        # Convert paths to relative paths for VMAT content
        rel_textures = {
            key: os.path.relpath(self._complete_texture_path(subdir, texture), self.input_dir).replace("\\", "/")
            for key, texture in texture_set.items()}

        # Create the output .vmat file with the correct name
        vmat_content = self._generate_vmat_content(
            base_name,
            rel_textures.get("color", ""),
            rel_textures.get("heightmap", ""),
            rel_textures.get("metalness_emissive_roughness", ""),
            os.path.relpath(translucency_path, self.input_dir).replace("\\", "/") if translucency_path else None
        )

        output_file_path = os.path.join(output_dir_path, f"{"pbr_" + base_name}.vmat")

        # Check if the file path ends with ".texture.vmat" and replace if necessary
        if output_file_path.endswith(".texture.vmat"):
            output_file_path = output_file_path.replace(".texture.vmat", ".vmat")

        with open(output_file_path, 'w') as vmat_file:
            vmat_file.write(vmat_content)
        print(f"Generated {output_file_path}")

    def _complete_texture_path(self, subdir, texture_name):
        """Ensure that the texture path has the correct file extension."""
        texture_path = os.path.join(subdir, texture_name)
        if not os.path.exists(texture_path):
            if os.path.exists(f"{texture_path}.tga"):
                return f"{texture_path}.tga"
            elif os.path.exists(f"{texture_path}.png"):
                return f"{texture_path}.png"
        return texture_path

    def _generate_translucency_map(self, color_path):
        try:
            img = Image.open(color_path).convert("RGBA")
            alpha = img.getchannel("A")

            # Create the binary translucency map
            trans_img = Image.eval(alpha, lambda a: 255 if a > 0 else 0)

            # Check if the image is fully black
            if trans_img.getextrema() == (0, 0):
                return None  # Fully black, no need to create the file

            trans_path = color_path.replace('.png', '_trans.png')
            trans_img.save(trans_path)
            return trans_path
        except Exception as e:
            print(f"Failed to generate translucency map for {color_path}: {e}")
            return None

    def _generate_vmat_content(self, base_name, color_texture, heightmap_normal, metalness_emissive_roughness,
                               translucency_path):
        vmat_template = f"""
// THIS FILE IS AUTO-GENERATED

Layer0
{{
    shader "csgo_lightmappedgeneric.vfx"

    //---- Color ----
    g_flModelTintAmount "1.000"
    g_flVertexColorOpacityScale "1.000"
    g_vColorTint "[1.000000 1.000000 1.000000 0.000000]"

    //---- Fog ----
    g_bFogEnabled "1"

    //---- Lighting ----
    g_flMetalness "0.000"

    //---- PBR 1 ----
    g_vLayer1Tint "[1.000000 1.000000 1.000000 0.000000]"
    TextureLayer1AmbientOcclusion "materials/default/default_ao.tga"
    TextureLayer1Color "{color_texture}"
    TextureLayer1Normal "{heightmap_normal}"
    TextureLayer1Roughness "{metalness_emissive_roughness}"
"""
        if translucency_path:
            vmat_template += f"""
    //---- Translucent ----
    F_TRANSLUCENT 1
    TextureLayer1Translucency "{translucency_path}"
"""
        vmat_template += """
    //---- Texture Address Mode ----
    g_nTextureAddressModeU "0" // Wrap
    g_nTextureAddressModeV "0" // Wrap

    //---- Translucent ----
    g_flOpacityScale "1.000"

    VariableState
    {
        "Color"
        {
        }
        "Fog"
        {
        }
        "Lighting"
        {
            "Metalness" 0
        }
        "PBR 1"
        {
            "Albedo" 0
            "Albedo Translucency" 0
            "Normal" 0
            "Roughness" 0
            "Ambient Occlusion" 0
        }
        "Texture Address Mode"
        {
        }
        "Translucent"
        {
        }
    }
}}"""
        return vmat_template

    def _copy_texture_files(self, file_paths, output_dir_path):
        for file_path in file_paths:
            if file_path and os.path.exists(file_path):
                os.path.relpath(file_path, self.input_dir)
                destination_path = os.path.join(output_dir_path, os.path.basename(file_path))
                shutil.copy2(file_path, destination_path)
                print(f"Copied {file_path} to {destination_path}")
