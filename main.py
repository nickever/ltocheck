#!/usr/bin/env python3

"""
Command line interface and GUI tool to compare a master csv to an LTO csv.
Compares file size, frame quantity and MD5 Hash.
"""

# Import from Python Standard Library
import gui
import argparse
import datetime

# Import from this package
import ltocheck_cli

__author__ = "Nick Everett"
__version__ = "1.0"
__license__ = "GNU GPLv3"


def parse_args():
    """
    Command line arguments: the tool takes two compulsory arguments as strings (csv file paths in order master/lto),
    an optional output file path.
    """
    out_filename = "lto_check_report_{:%Y-%m-%d_%H%M}.csv".format(datetime.datetime.today())

    description = (
        'Command line interface tool to compare a master csv with an LTO csv'
        '\nhttps://github.com/nickever/lto_check')

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-m", "--master_csv_path", type=str,
                        help="master csv input file path (required)")
    parser.add_argument("-l", "--lto_csv_path", type=str,
                        help="LTO csv input file path (required)")
    parser.add_argument("-d", "--out_path", action="store", default='.',
                        help="output destination path")
    parser.add_argument("-o", "--out_name", action="store", default=out_filename,
                        help="output filename")
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="verbosity (-v) or debug mode (-vv)")
    parser.add_argument(
        "--version",
        action="version",
        version="{} (version {})".format("%(prog)s", __version__))
    args = parser.parse_args()
    return args


def main():
    args = parse_args()  # Read the command-line arguments

    if args.master_csv_path and args.lto_csv_path:              # If there is an argument,
        ltocheck_cli.check(args)      # run the command-line version
    else:
        gui.vp_start_gui()      # otherwise run the GUI version


if __name__ == "__main__":
    main()

