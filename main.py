from image_scaling import scale_images_in_directory, scale_single_image
from vmat_writer import create_vmat_files
from fbx_splitter import create_subdirectories_with_files
from model_writer import traverse_and_generate_models
from pbr_texture_creator import TextureSetFinder
from vmdl_remapper import VmdlProcessor

# Example usage for scaling a single file
# single_file_path = 'your_single_file_path'
# scale_single_image(single_file_path, max_size=(10000, 10000), max_size_output=(2048, 2048))

# Example usage for creating VMAT files
# create_vmat_files(
#    "D:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\content\\csgo_addons\\de_anubis_minecraft",
#    "D:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\content\\csgo_addons\\de_anubis_minecraft")

# Example usage for scaling images in a directory
# Uncomment and replace 'your_project_directory' with the actual directory path
# scale_images_in_directory(
#    "D:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\content\\csgo_addons\\de_anubis_minecraft\\models",
#    required_substring=None, max_size_output=(1024, 1024), max_size=(1024, 1024), min_size=(1, 1))

# Example usage for splitting FBX files into subdirectories
# Uncomment and replace 'your_fbx_directory' with the actual directory path
# create_subdirectories_with_files(
# "D:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\content\\csgo_addons\\de_anubis_minecraft\\models\\details\\fbx",
# 2000)

# Example usage for traversing directories and generating models
# Uncomment and replace 'your_model_directory' with the actual directory path
# traverse_and_generate_models(
# "D:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\content\\csgo_addons\\de_anubis_minecraft\\models\\details\\fbx")

finder = TextureSetFinder('C:\\Users\\misch\\Downloads\\Vanilla-PBR-Deferred-Lighting-v2.2',
                         'C:\\Users\\misch\\Downloads\\test')
finder.find_texture_sets()

# scale_images_in_directory(
#    "D:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\content\\csgo_addons\\de_anubis_minecraft\\materials\\pbr_minecraft",
#    required_substring=None, max_size_output=(1024, 1024), max_size=(1024, 1024), min_size=(1, 1), scale_factor=64)

#processor = VmdlProcessor("C:\\Users\\misch\\Downloads\\test1", "C:\\Users\\misch\\Downloads\\test1",
#                          "D:\\SteamLibrary\\steamapps\\common\\Counter-Strike Global Offensive\\content\\csgo_addons\\de_anubis_minecraft")
#processor.process_vmdl_files()
