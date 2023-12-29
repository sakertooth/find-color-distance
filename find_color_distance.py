from ast import literal_eval
from tabulate import tabulate
import argparse
import re
import sys
import math

def color_from_input(color_input):
    tuple_match = re.match(r"\( *(\d*) *, *(\d*) *, *(\d*) *\)", color_input)
    hex_match = re.match(
        r"#([0-9a-fA-F][0-9a-fA-F])([0-9a-fA-F][0-9a-fA-F])([0-9a-fA-F][0-9a-fA-F])",
        color_input,
    )

    if tuple_match != None:
        red, green, blue = tuple_match.groups()
    elif hex_match != None:
        red, green, blue = [int(val, 16) for val in hex_match.groups()]
    else:
        raise RuntimeError(f"Invalid color input: {color_input}")
    return {"input": color_input.strip(), "red": int(red), "green": int(green), "blue": int(blue)}

def find_distance(target, color):
    target_point = (target['red'], target['green'], target['blue'])
    color_point = (color['red'], color['green'], color['blue'])
    color_distance_from_target = math.dist(color_point, target_point)
    return (target['input'], color['input'], f'{round(color_distance_from_target, 2)}')

parser = argparse.ArgumentParser(
    prog="Color Distance Calculator",
    description="Calculates the distance between a palette of target colors and of other colors",
)

parser.add_argument(
    "targets",
    help="The target colors (either list of (red, green, blue) or hex values)",
    nargs="+"
)

parser.add_argument(
    "palette",
    nargs="+",
    help="Color palette (list of (red, green, blue) or hex values), reads from stdin if - is given",
)

args = parser.parse_args()

if args.palette == None and args.infile == None:
    raise RuntimeError("At least one must be specified: palette, infile")

targets = [color_from_input(color) for color in args.targets]

palette = []
if '-' in args.palette:
    palette.extend([color_from_input(line) for line in sys.stdin])
else:
    palette.extend([color_from_input(color) for color in args.palette if color != '-'])

results = [find_distance(target, color) for color in palette for target in targets]
print(tabulate(results, headers=['Target', 'Color', 'Distance']))
