#!/usr/bin/env python3

"""
Command line interface tool to compare a master csv to an LTO csv.
Compares file size, frame quantity and MD5 Hash.
"""

import csv
import sys
import argparse
import datetime
import collections
from collections import OrderedDict

__author__ = "Nick Everett"
__version__ = "0.5.2"
__license__ = "GNU GPLv3"


def _read_ss_csv(input_file):
    """
    Opens a SS csv as a dictionary with header as key, sorts by given column key, outputs filtered dictionary
    """
    with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            reader = sorted(reader, key=lambda row: row['Name'])
            filtered_dict = []

            def _filter_dict_ss(row):
                if row['Frames'] is not "" \
                        and row['Frames'] is not "1":
                    return row

            for row in filter(_filter_dict_ss, reader):
                filtered_row = collections.OrderedDict([("Name", row['Name'].split('.')[0]),
                                                        ("Frames", row['Frames']),
                                                        ("Size", row['File Size'])])
                filtered_dict.append(filtered_row)
    f.close()
    return filtered_dict, len(filtered_dict)


def _read_lto_csv(input_file):
    """
    Opens an LTO csv as a dictionary with header as key, sorts by given column key, outputs filtered dictionary
    """
    with open(input_file, 'r') as f:
        reader = csv.DictReader(f)
        reader = sorted(reader, key=lambda row: row['Name'])
        filtered_dict = []

        def _filter_dict_lto(row):
            if "CAMERA_MASTER" in row['Path'] \
                    and row['Frames'] is not "" \
                    and row['Frames'] is not "1":
                return row
        for row in filter(_filter_dict_lto, reader):
            filtered_row = collections.OrderedDict([("Name", row['Name'].split('.')[0]),
                                                    ("Frames", row['Frames']),
                                                    ("Size", row['Size']),
                                                    ("Media", row['Media'])])
            filtered_dict.append(filtered_row)
    f.close()
    return filtered_dict, len(filtered_dict)


def _compare_dicts(args, dict1, dict2):
    """
    Compares two given dictionaries, returns quanity of matches, non matches and not found files
    as well as outputting data to the results printer func and csv creator
    """
    match = 0
    non_match = 0
    not_found = 0
    output_file = "{}/{}".format(args.out_path.strip('/'), args.out_name)
    for row1 in dict1:
        file_found = False
        for row2 in dict2:
            if row1['Name'] in row2['Name']:
                file_found = True
                match_status = ""
                error_message = ""
                if row1["Frames"] in row2["Frames"] and row1["Size"] in row2["Size"]:
                    match += 1
                    match_status = "MATCH"
                else:
                    if row1["Frames"] not in row2["Frames"]:
                        non_match += 1
                        match_status = "ERROR"
                        error_message += "FRAME COUNT MISMATCH \t"
                    if row1["Size"] not in row2["Size"]:
                        non_match += 1
                        match_status = "ERROR"
                        error_message += "SIZE MISMATCH \t"
                _write_csv(output_file, row1, row2, match_status, error_message)
                _results_printer(row1, row2, match_status, error_message)
        if file_found is False:
            not_found += 1
            _write_csv(output_file, row1, None, "ERROR", "FILE NOT FOUND ")
            _results_printer(row1, None, "ERROR", "FILE NOT FOUND ")
    return match, non_match, not_found


first_write = True


def _write_csv(output_filepath, row1, row2, match_status, error_message):
    global first_write
    with open(output_filepath, 'a+') as f:
        fieldnames = ["STATUS",
                      "FILENAME",
                      "FRAMES_MASTER",
                      "FRAMES_LTO",
                      "SIZE_MASTER",
                      "SIZE_LTO",
                      "LTO_TAPE",
                      "ERROR MESSAGES",]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if first_write is True:
            writer.writeheader()
            first_write = False
            pass
        else:
            pass
        if row2 is not None:
            writer.writerow({'STATUS': match_status,
                             'FILENAME': row1['Name'],
                             'FRAMES_MASTER': row1['Frames'],
                             'FRAMES_LTO': row2['Frames'],
                             'SIZE_MASTER': row1['Size'],
                             'SIZE_LTO': row2['Size'],
                             'LTO_TAPE': row2['Media'],
                             'ERROR MESSAGES': error_message})
        else:
            writer.writerow({'STATUS': match_status,
                             'FILENAME': row1['Name'],
                             'FRAMES_MASTER': row1['Frames'],
                             'SIZE_MASTER': row1['Size'],
                             'ERROR MESSAGES': error_message})
    f.close()


first_print = True


def _results_printer(row1, row2, match_status, error_message):
    """
    Prints data to terminal provided by the compare_dicts function
    """
    global first_print
    if first_print is True:
        print("\n\t{: ^6} | {: ^24} {: ^15} {: ^15} {: ^14} {: ^14} {: ^8}  |\n"
              "\t       |{: ^98}|"
              .format("STATUS",
                      "FILENAME",
                      "FRAMES_MASTER",
                      "FRAMES_LTO",
                      "SIZE_MASTER",
                      "SIZE_LTO",
                      "LTO_TAPE",
                      " "))
        first_print = False
        pass
    else:
        pass
    if row2 is not None:
        print("\t{: ^6} | {: ^24} {: ^15} {: ^15} {: ^14} {: ^14} {: ^8}  |\t {}\n"
              "\t       |{: ^98}|"
              .format(match_status,
                      row1['Name'],
                      row1['Frames'],
                      row2['Frames'],
                      row1['Size'],
                      row2['Size'],
                      row2['Media'],
                      error_message,
                      " "))
    else:
        print("\t{: ^6} | {: ^24} {: ^15} {: ^15} {: ^14} {: ^14} {: ^8}  |\t {}\n"
              "\t       |{: ^98}|"
              .format(match_status,
                      row1['Name'],
                      row1['Frames'],
                      " ",
                      row1['Size'],
                      " ",
                      " ",
                      error_message,
                      " "))


def _summary_printer(int1, int2, int3, int4, int5):
    print("\nTotal Video Files on Master: {}"
          "\nTotal Video Files on LTO: {}"
          "\nMatches: {}"
          "\nNon-Matches: {}"
          "\nNot Found: {}"
          .format(int1, int2, int3, int4, int5))


def parse_args():
    """
    Command line arguments: the tool takes two compulsory arguments as strings (csv file paths in order master/lto),
    an optional output file path.
    """
    description = (
        'Command line interface tool to compare a master csv with an LTO csv'
        '- https://github.com/nickever/lto_check')
    parser = argparse.ArgumentParser(description=description, usage='%(prog)s [-h] [-o] [-d] [-v] [--version] '
                                                                    'master_csv_path  LTO_csv_path')
    parser.add_argument("master_csv_path", type=str,
                        help="master csv input file path (required)")
    parser.add_argument("LTO_csv_path", type=str,
                        help="LTO csv input file path (required)")
    parser.add_argument("-d", "--out_path", action="store", default='.',
                        help="output destination path", metavar='')
    out_filename = "lto_check_report_{:%Y-%m-%d_%H%M}.csv".format(datetime.datetime.today())
    parser.add_argument("-o", "--out_name", action="store", default=out_filename,
                        help="output filename", metavar='')
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="verbosity (-v, -vv, etc)")
    parser.add_argument(
        "--version",
        action="version",
        version="{} (version {})".format("%(prog)s", __version__))
    return parser.parse_args()


def main():
    args = parse_args()
    csv1 = args.master_csv_path
    csv2 = args.LTO_csv_path
    try:
        master_media_files, count_mmf = _read_ss_csv(csv1)
        lto_media_files, count_lmf = _read_lto_csv(csv2)
        files_matched, files_non_matched, files_not_found = _compare_dicts(args, master_media_files, lto_media_files)
        _summary_printer(count_mmf, count_lmf, files_matched, files_non_matched, files_not_found)
    except KeyboardInterrupt:
        sys.exit("Exiting...")
    except FileNotFoundError as e:
        sys.exit("File not found: {}\nExiting...".format(str(e).split("'")[-2]))
    except KeyError as e:
        sys.exit('Failed to find column: {}'.format(e))


if __name__ == "__main__":      # executed when run from the command line
    main()
