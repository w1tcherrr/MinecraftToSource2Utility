import os
from PIL import Image


def generate_vmat_content(png_relative_path):
    """
    Generate the content of the .vmat file based on the .png file's relative path.

    :param png_relative_path: The relative path to the .png file from the root directory.
    :return: The content for the .vmat file as a string.
    """
    return f"""// THIS FILE IS AUTO-GENERATED

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
    TextureLayer1Color "{png_relative_path}"
    TextureLayer1Normal "materials/default/default_normal.tga"
    TextureLayer1Roughness "materials/default/default_rough.tga"

    //---- Texture Address Mode ----
    g_nTextureAddressModeU "0" // Wrap
    g_nTextureAddressModeV "0" // Wrap


    VariableState
    {{
        "Color"
        {{
        }}
        "Fog"
        {{
        }}
        "Lighting"
        {{
            "Metalness" 0
        }}
        "PBR 1"
        {{
            "Albedo" 0
            "Normal" 0
            "Roughness" 0
            "Ambient Occlusion" 0
        }}
        "Texture Address Mode"
        {{
        }}
    }}
}}
"""


def create_trans_png(source_png_path, trans_png_path):
    """
    Create the _trans.png file by copying the original png and modifying its pixels.
    :param source_png_path: The path to the original .png file.
    :param trans_png_path: The path to the _trans.png file to be created.
    """
    with Image.open(source_png_path) as img:
        trans_img = img.copy()
        trans_img = trans_img.convert("RGBA")
        data = trans_img.getdata()

        new_data = []
        for item in data:
            if item[0] == 0 and item[1] == 0 and item[2] == 0:
                new_data.append((0, 0, 0, item[3]))
            else:
                new_data.append((255, 255, 255, item[3]))

        trans_img.putdata(new_data)
        trans_img.save(trans_png_path)


def remove_translucency(png_path):
    """
    Remove any translucency information from the .png file.
    :param png_path: The path to the .png file to be modified.
    """
    with Image.open(png_path) as img:
        img = img.convert("RGBA")
        data = img.getdata()

        new_data = []
        for item in data:
            new_data.append((item[0], item[1], item[2], 255))

        img.putdata(new_data)
        img.save(png_path)


def create_vmat_files(source_directory, target_directory):
    """
    Traverse the source directory to find .png files and create corresponding .vmat files in the target directory.

    :param source_directory: The directory containing the .png files.
    :param target_directory: The directory where the .vmat files will be created.
    """
    os.makedirs(target_directory, exist_ok=True)

    for root, _, files in os.walk(source_directory):
        for file in files:
            if file.lower().endswith('.png'):
                full_png_path = os.path.join(root, file)
                relative_png_path = os.path.relpath(full_png_path, source_directory)
                relative_png_path = relative_png_path.replace('\\', '/')

                remove_translucency(full_png_path)
                print(f"Translucency removed from {full_png_path}")

                try:
                    parts = relative_png_path.split('/tex/')
                    if len(parts) > 1:
                        subfolders = parts[1].rsplit('/', 1)[0]
                        prefix = f"{subfolders.replace('/', '_')}_"
                    else:
                        prefix = ''
                except IndexError:
                    prefix = ''

                if prefix.endswith('_'):
                    prefix = prefix[:-1] + '-'

                vmat_filename = prefix + os.path.splitext(file)[0] + '.vmat'

                if vmat_filename.startswith("jmc2obj_banner_"):
                    vmat_filename = vmat_filename.replace("jmc2obj_banner_", "jmc2obj_banner-banner_")

                if vmat_filename.startswith("minecraft_entity_"):
                    vmat_filename = vmat_filename.replace("minecraft_entity_", "minecraft_entity-")

                vmat_filename = vmat_filename.replace("player_wide-steve", "player-wide-steve")

                vmat_filepath = os.path.join(target_directory, vmat_filename)

                if not os.path.exists(vmat_filepath):
                    with open(vmat_filepath, 'w') as vmat_file:
                        vmat_content = generate_vmat_content(relative_png_path)
                        vmat_file.write(vmat_content)
                        print(f"Generated {vmat_filepath}")
                else:
                    print(f"Skipped {vmat_filepath} as it already exists")

                trans_png_filename = os.path.splitext(file)[0] + '_trans.png'
                trans_png_filepath = os.path.join(root, trans_png_filename)

                if not os.path.exists(trans_png_filepath):
                    create_trans_png(full_png_path, trans_png_filepath)
                    print(f"Created {trans_png_filepath}")
                else:
                    print(f"Skipped {trans_png_filepath} as it already exists")
