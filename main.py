from image_scaling import scale_images_in_directory, scale_single_image
from vmat_writer import create_vmat_files
from fbx_splitter import create_subdirectories_with_files
from model_writer import traverse_and_generate_models

# Example usage for scaling images in a directory
# Uncomment and replace 'your_project_directory' with the actual directory path
# scale_images_in_directory("your_project_directory", required_substring=None, max_size_output=(256, 256),
#                          max_size=(256, 256), min_size=(1, 1))

# Example usage for scaling a single file
# single_file_path = 'your_single_file_path'
# scale_single_image(single_file_path, max_size=(10000, 10000), max_size_output=(2048, 2048))

# Example usage for creating VMAT files
# create_vmat_files(
#     "your_project_directory",
#     "your_project_directory")

# Example usage for splitting FBX files into subdirectories
# Uncomment and replace 'your_fbx_directory' with the actual directory path
# create_subdirectories_with_files(
#  "your_fbx_directory",
#  2000)

# Example usage for traversing directories and generating models
# Uncomment and replace 'your_model_directory' with the actual directory path
# traverse_and_generate_models(
#  "your_model_directory")
