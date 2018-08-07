import argparse
from PIL import Image
import os
import sys


def get_console_params():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path_to_file",
        type=str,
        help="path to initial image, require .jpg and .png format")
    parser.add_argument(
        "-w", "--width",
        type=int,
        help="final image width")
    parser.add_argument(
        "-he", "--height",
        type=int,
        help="final image height")
    parser.add_argument(
        "-s", "--scale",
        type=float,
        help="keep proportion and zoom image")
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=os.getcwd(), help="path to save final image")
    return parser


def check_params_conflicts(width, height, scale):
    if ((width is not None or height is not None) and
            scale is not None):
        raise argparse.ArgumentTypeError(
            "-h and -w parameters are conflicted with -s")
    if not (width is not None or height is not None or
            scale is not None):
        raise argparse.ArgumentTypeError("There is not enough parameters")
    if (width == 0 or height == 0 or scale == 0):
        raise argparse.ArgumentTypeError("0 is not acceptable as a parameter")
    return False


def define_request_params(args, initial_image_size):
    initial_image_width, initial_image_height = initial_image_size
    if args.width and args.height:
        final_image_height = args.height
        final_image_width = args.width
    elif args.scale:
        final_image_width = initial_image_width * args.scale
        final_image_height = initial_image_height * args.scale
    elif args.width or args.height:
        if args.width is not None:
            final_image_width = args.width
            final_image_height = (final_image_width/initial_image_width
                * initial_image_height)
        else:
            final_image_height = args.height
            final_image_width = (final_image_height/initial_image_height
                * initial_image_width)
    return int(final_image_width), int(final_image_height)


def get_initial_image(path):
    initial_image = Image.open(path)
    return initial_image


def resize_image(path_to_original, path_to_result, final_image_size):
    final_image_width, final_image_height = final_image_size
    initial_image = get_initial_image(path_to_original)
    final_image = initial_image.resize(final_image_size)
    return final_image


def save_image(
        final_image, initial_image_name,
        path_to_save, final_image_size):
    final_image_width, final_image_height = final_image_size
    image_name, ext = os.path.splitext(initial_image_name)
    path_to_final_file = os.path.join(
        path_to_save,
        "{}__{}x{}{}".format(
            image_name, final_image_width, final_image_height, ext))
    final_image.save(path_to_final_file)


if __name__ == "__main__":
    parser = get_console_params()
    args = parser.parse_args()
    try:
        check_params_conflicts(args.width, args.height, args.scale)
        initial_image_size = get_initial_image(args.path_to_file).size
        final_image_size = define_request_params(args, initial_image_size)
        final_image = resize_image(
            args.path_to_file, args.output, final_image_size)
    except (FileNotFoundError, ValueError, argparse.ArgumentTypeError) as e:
        sys.exit(e)
    initial_image_name = os.path.basename(args.path_to_file)
    initial_image_width, initial_image_height = initial_image_size
    final_image_width, final_image_height = final_image_size
    if (initial_image_width/initial_image_height !=
            (final_image_width/final_image_height)):
        print("The scale of final image is not the same")
    save_image(
        final_image, initial_image_name,
        args.output, final_image_size)
