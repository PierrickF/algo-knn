import re
import math
import argparse


def check_hexacolor(color_str):
    """Check wether the value given for fur_color is a valid hexadecimal color code."""

    valid_code = re.compile("^#([a-zA-Z]|[0-9]){6}")        # regex for #aBc123

    if valid_code.fullmatch(color_str):
        return True


def euclidean_distance(p_x, p_y, q_x, q_y):
    """Compute the distance between two points on a 2D plane."""
    # p_x is bmi, and p_y is fur_color_int of monkey 1
    # q_x is bmi, and q_y is fur_color_int of monkey 2
    return math.sqrt((p_x - q_x)**2 + (p_y - q_y)**2)


def get_cli_args():
    """Argument parser which accepts as arguments a path to an input CSV,
    and a path to an output CSV."""

    # create an argument parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subparser")

    # create the knn subparser
    knn = subparsers.add_parser("knn")

    # add arguments to the knn subparser
    knn.add_argument("input", default=1, help="path to an input CSV", type=str)
    knn.add_argument("output", default=1, help="path to an output CSV", type=str)

    # create the visualize subparser
    visualize = subparsers.add_parser("visualize")

    # add arguments to the visualize subparser
    visualize.add_argument("input", help="path to an input CSV", type=str)
    visualize.add_argument("columns", help="valid column names", type=str,
                           nargs=2,
                           choices=["size", "weight"])

    # parse the arguments
    args = parser.parse_args()

    # it's what pirates say
    return args
