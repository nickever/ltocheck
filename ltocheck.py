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


def _compare_dicts(args, ss_dict, lto_dict):
    """
    Compares two given dictionaries, returns quanity of matches, non matches and not found files
    as well as outputting data to the results printer func and csv creator
    """
    match = 0
    non_match = 0
    not_found = 0
    output_file = "{}/{}".format(args.out_path.strip('/'), args.out_name)
    for ss_row in ss_dict:
        file_found = False
        for lto_row in lto_dict:
            if ss_row['Name'] in lto_row['Name']:
                file_found = True
                match_status = ""
                error_message = ""
                if ss_row["Frames"] in lto_row["Frames"] and ss_row["Size"] in lto_row["Size"]:
                    match += 1
                    match_status = "MATCH"
                else:
                    if ss_row["Frames"] not in lto_row["Frames"]:
                        non_match += 1
                        match_status = "ERROR"
                        error_message += "FRAME COUNT MISMATCH \t"
                    if ss_row["Size"] not in lto_row["Size"]:
                        non_match += 1
                        match_status = "ERROR"
                        error_message += "SIZE MISMATCH \t"
                _write_csv(output_file, ss_row, lto_row, match_status, error_message)
                _results_printer(ss_row, lto_row, match_status, error_message)
        if file_found is False:
            not_found += 1
            _write_csv(output_file, ss_row, None, "ERROR", "FILE NOT FOUND ")
            _results_printer(ss_row, None, "ERROR", "FILE NOT FOUND ")
    return match, non_match, not_found


first_write = True


def _write_csv(output_filepath, ss_row, lto_row, match_status, error_message):
    global first_write
    with open(output_filepath, 'a+') as f:
        with open(output_filepath, 'r') as f2:
            fieldnames = ["STATUS",
                          "FILENAME",
                          "FRAMES_MASTER",
                          "FRAMES_LTO",
                          "SIZE_MASTER",
                          "SIZE_LTO",
                          "LTO_TAPE",
                          "ERROR MESSAGES"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            if first_write is True:
                writer.writeheader()
                first_write = False
            else:
                pass
            if ss_row['Name'] not in f2.read():
                if lto_row is not None:
                    writer.writerow({'STATUS': match_status,
                                     'FILENAME': ss_row['Name'],
                                     'FRAMES_MASTER': ss_row['Frames'],
                                     'FRAMES_LTO': lto_row['Frames'],
                                     'SIZE_MASTER': ss_row['Size'],
                                     'SIZE_LTO': lto_row['Size'],
                                     'LTO_TAPE': lto_row['Media'],
                                     'ERROR MESSAGES': error_message})
                else:
                    writer.writerow({'STATUS': match_status,
                                     'FILENAME': ss_row['Name'],
                                     'FRAMES_MASTER': ss_row['Frames'],
                                     'SIZE_MASTER': ss_row['Size'],
                                     'ERROR MESSAGES': error_message})
            else:
                pass
                #print("{} already in file".format(lto_row['Name']))
    f.close()


first_print = True


def _results_printer(ss_row, lto_row, match_status, error_message):
    """
    Prints data to terminal provided by the compare_dicts function
    """
    global first_print
    if first_print is True:
        _vprint("\n\t{: ^6} | {: ^24} {: ^15} {: ^15} {: ^14} {: ^14} {: ^8}  |\n"
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
    if lto_row is not None:
        _vprint("\t{: ^6} | {: ^24} {: ^15} {: ^15} {: ^14} {: ^14} {: ^8}  |\t {}\n"
              "\t       |{: ^98}|"
              .format(match_status,
                      ss_row['Name'],
                      ss_row['Frames'],
                      lto_row['Frames'],
                      ss_row['Size'],
                      lto_row['Size'],
                      lto_row['Media'],
                      error_message,
                      " "))
    else:
        _vprint("\t{: ^6} | {: ^24} {: ^15} {: ^15} {: ^14} {: ^14} {: ^8}  |\t {}\n"
              "\t       |{: ^98}|"
              .format(match_status,
                      ss_row['Name'],
                      ss_row['Frames'],
                      " ",
                      ss_row['Size'],
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
        action="store_true",
        default=False,
        help="verbosity")
    parser.add_argument(
        "--version",
        action="version",
        version="{} (version {})".format("%(prog)s", __version__))
    return parser.parse_args()


if parse_args().verbose:
    def _vprint(*args, **kwargs):
        print(*args, **kwargs)
else:
    _vprint = lambda *a, **k: None


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
