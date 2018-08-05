import argparse
from PIL import Image
import os
import sys


def get_console_params():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path_to_file", type=str,
        help="path to initial image, require .jpg and .png format")
    parser.add_argument(
        "-w", "--width", type=int,
        help="final image width")
    parser.add_argument(
        "-he", "--height", type=int,
        help="final image height")
    parser.add_argument(
        "-s", "--scale", type=float,
        help="keep proportion and zoom image")
    parser.add_argument(
        "-o", "--output", type=str,
        default=os.getcwd(), help="path to save final image")
    return parser


def define_request_params(namespace, initial_image_size):
    print(namespace)
    initial_image_width, initial_image_height = initial_image_size
    if (namespace.width or namespace.height) and namespace.scale:
        print("-h and -w parameters are conflicted with -s")
        return None
    elif namespace.width and namespace.height:
        final_image_height = namespace.height
        final_image_width = namespace.width
        if (initial_image_width/initial_image_height !=
                (final_image_width/final_image_height)):
            print("The scale of final image is not the same")
    elif namespace.scale:
        final_image_width = initial_image_width * namespace.scale
        final_image_height = initial_image_height * namespace.scale
    elif namespace.width or namespace.height:
        if namespace.width is not None:
            final_image_width = namespace.width
            final_image_height = (final_image_width /
                                  initial_image_width *
                                  initial_image_height)
        else:
            final_image_height = namespace.height
            final_image_width = (final_image_height /
                                 initial_image_height *
                                 initial_image_width)
    else:
        print("There is not enough parameters")
        return None
    print(final_image_width, final_image_height)
    return int(final_image_width), int(final_image_height)


def get_initial_image_size(path):
    initial_image = Image.open(path)
    return initial_image.size


def resize_image(path_to_original, path_to_result, final_image_size):
    final_image_width, final_image_height = final_image_size
    initial_image = Image.open(path_to_original)
    final_image = initial_image.resize(final_image_size)
    return final_image


def save_image(
        final_image, initial_image_name, ext,
        path_to_save, final_image_size):
    final_image_width, final_image_height = final_image_size
    if ext == ".jpg":
        ext = ".JPEG"
    path_to_final_file = os.path.join(
        path_to_save,
        initial_image_name+"__{}x{}{}".format(
            final_image_width, final_image_height, ext))
    final_image.save(path_to_final_file, ext[1:])


if __name__ == "__main__":
    parser = get_console_params()
    namespace = parser.parse_args()
    try:
        initial_image_size = get_initial_image_size(namespace.path_to_file)
    except FileNotFoundError:
        sys.exit("File not found")
    initial_image_name, ext = os.path.splitext(
        str.split(sys.argv[1], "\\")[-1])
    final_image_size = define_request_params(namespace, initial_image_size)
    if final_image_size is not None:
        final_image = resize_image(
            namespace.path_to_file, namespace.output, final_image_size)
    else:
        sys.exit()
    save_image(
        final_image, initial_image_name, ext,
        namespace.output, final_image_size)
