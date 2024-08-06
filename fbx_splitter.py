import os
import shutil


def create_subdirectories_with_files(directory: str, num_files: int):

    if not os.path.isdir(directory):
        raise ValueError(f"The directory {directory} does not exist.")

    fbx_files = [f for f in os.listdir(directory) if f.endswith('.fbx')]

    if len(fbx_files) < num_files:
        raise ValueError(
            f"There are not enough .fbx files in the directory to distribute {num_files} files per subdirectory.")

    subdir_index = 1
    for i in range(0, len(fbx_files), num_files):
        subdir_name = os.path.join(directory, str(subdir_index))
        os.makedirs(subdir_name, exist_ok=True)

        for fbx_file in fbx_files[i:i + num_files]:
            src = os.path.join(directory, fbx_file)
            dst = os.path.join(subdir_name, fbx_file)
            shutil.move(src, dst)

        subdir_index += 1
