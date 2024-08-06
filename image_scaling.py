import os
from PIL import Image
import glob


def scale_images_in_directory(input_pattern, scale_factor=8, max_size=(32, 32), min_size=(0, 0),
                              required_substring=None, max_size_output=None):
    for input_directory in glob.glob(input_pattern):
        for root, _, files in os.walk(input_directory):
            for filename in files:
                if filename.lower().endswith('.png') and (required_substring is None or required_substring in filename):
                    input_filepath = os.path.join(root, filename)
                    try:
                        with Image.open(input_filepath) as img:
                            if max_size[0] >= img.width >= min_size[0] and max_size[1] >= img.height >= min_size[1]:
                                new_size = (img.width * scale_factor, img.height * scale_factor)
                                if max_size_output:
                                    aspect_ratio = img.width / img.height
                                    if new_size[0] > max_size_output[0] or new_size[1] > max_size_output[1]:
                                        if aspect_ratio > 1:
                                            new_size = (max_size_output[0], int(max_size_output[0] / aspect_ratio))
                                        else:
                                            new_size = (int(max_size_output[1] * aspect_ratio), max_size_output[1])
                                scaled_img = img.resize(new_size, Image.NEAREST)
                                scaled_img.save(input_filepath)
                                print(f"Scaled {filename} to {new_size} and overwrote the original file.")
                            else:
                                print(f"Skipped {filename} because its size is greater than {max_size}.")
                    except Exception as e:
                        print(f"Could not process {filename}: {e}")


def scale_single_image(input_filepath, scale_factor=8, max_size=(32, 32), max_size_output=None):
    if input_filepath.lower().endswith('.png'):
        try:
            with Image.open(input_filepath) as img:
                if img.width <= max_size[0] and img.height <= max_size[1]:
                    new_size = (img.width * scale_factor, img.height * scale_factor)
                    if max_size_output:
                        aspect_ratio = img.width / img.height
                        if new_size[0] > max_size_output[0] or new_size[1] > max_size_output[1]:
                            if aspect_ratio > 1:
                                new_size = (max_size_output[0], int(max_size_output[0] / aspect_ratio))
                            else:
                                new_size = (int(max_size_output[1] * aspect_ratio), max_size_output[1])
                    scaled_img = img.resize(new_size, Image.NEAREST)
                    scaled_img.save(input_filepath)
                    print(f"Scaled {os.path.basename(input_filepath)} to {new_size} and overwrote the original file.")
                else:
                    print(f"Skipped {os.path.basename(input_filepath)} because its size is greater than {max_size}.")
        except Exception as e:
            print(f"Could not process {os.path.basename(input_filepath)}: {e}")
    else:
        print(f"File {os.path.basename(input_filepath)} is not a .png file.")
