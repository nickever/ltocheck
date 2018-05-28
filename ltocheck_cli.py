#!/usr/bin/env python3

"""
Command line interface tool to compare a master csv to an LTO csv.
Compares file size, frame quantity and MD5 Hash.
"""

# Import from Python Standard Library
import csv
import sys
import collections

# Import from the package


def _read_ss_csv(input_file, debug):
    """
    Opens a SS csv as a dictionary with header as key, sorts by given column key, outputs filtered dictionary
    """
    _dprinter("Attempting master csv read", debug)
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
                                                    ("Size", row['File Size']),
                                                    ("MD5", row['MD5'])])
            filtered_dict.append(filtered_row)
    f.close()
    _dprinter("Master csv read and sorted from path {}\n{} files found, {} video files filtered"
              .format(input_file, len(reader), len(filtered_dict)), debug)
    return filtered_dict, len(filtered_dict)


def _read_lto_csv(input_file, debug):
    """
    Opens an LTO csv as a dictionary with header as key, sorts by given column key, outputs filtered dictionary
    """
    _dprinter("Attempting LTO csv read", debug)
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
                                                    ("MD5", row['MD5']),
                                                    ("Media", row['Media'])])
            filtered_dict.append(filtered_row)
    f.close()
    _dprinter("LTO csv read and sorted from path {}\n{} files found, {} video files filtered"
              .format(input_file, len(reader), len(filtered_dict)), debug)
    return filtered_dict, len(filtered_dict)


def _compare_dicts(args, ss_dict, lto_dict, verbose, debug):
    """
    Compares two given dictionaries, returns quanity of matches, non matches and not found files
    as well as outputting data to the results printer func and csv creator
    """
    _dprinter("Attempting compare the csvs", debug)
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
                if ss_row["Frames"] == lto_row["Frames"] \
                        and ss_row["Size"] == lto_row["Size"] \
                        and ss_row["MD5"].upper() == lto_row["MD5"].upper():
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
                    if ss_row["MD5"] != lto_row["MD5"]:
                        non_match += 1
                        match_status = "ERROR"
                        error_message += "MD5 MISMATCH \t"
                _write_csv(output_file, ss_row, lto_row, match_status, error_message, debug)
                _results_printer(ss_row, lto_row, match_status, error_message, verbose, debug)
        if file_found is False:
            not_found += 1
            _write_csv(output_file, ss_row, None, "ERROR", "FILE NOT FOUND ", debug)
            _results_printer(ss_row, None, "ERROR", "FILE NOT FOUND ", verbose, debug)
    return match, non_match, not_found


first_write = True


def _write_csv(output_filepath, ss_row, lto_row, match_status, error_message, debug):
    global first_write
    _dprinter("Attempting to write output csv to {}".format(output_filepath), debug)
    with open(output_filepath, 'a+') as f:
        fieldnames = ["STATUS",
                      "FILENAME",
                      "FRAMES_MASTER",
                      "FRAMES_LTO",
                      "SIZE_MASTER",
                      "SIZE_LTO",
                      "MD5_MASTER",
                      "MD5_LTO",
                      "LTO_TAPE",
                      "ERROR MESSAGES"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if first_write is True:
            writer.writeheader()
            first_write = False
        else:
            pass
        if lto_row is not None:
            writer.writerow({'STATUS': match_status,
                             'FILENAME': ss_row['Name'],
                             'FRAMES_MASTER': ss_row['Frames'],
                             'FRAMES_LTO': lto_row['Frames'],
                             'SIZE_MASTER': ss_row['Size'],
                             'SIZE_LTO': lto_row['Size'],
                             'MD5_MASTER': ss_row['MD5'],
                             'MD5_LTO': lto_row['MD5'],
                             'LTO_TAPE': lto_row['Media'],
                             'ERROR MESSAGES': error_message})
        else:
            writer.writerow({'STATUS': match_status,
                             'FILENAME': ss_row['Name'],
                             'FRAMES_MASTER': ss_row['Frames'],
                             'SIZE_MASTER': ss_row['Size'],
                             'MD5_MASTER': ss_row['MD5'],
                             'ERROR MESSAGES': error_message})
    f.close()


first_print = True


def _results_printer(ss_row, lto_row, match_status, error_message, verbose, debug):
    """
    Prints data to terminal provided by the compare_dicts function
    """
    if verbose is True:
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
        if lto_row is not None:
            print("\t{: ^6} | {: ^24} {: ^15} {: ^15} {: ^14} {: ^14} {: ^8}  |\t {}\n"
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
            print("\t{: ^6} | {: ^24} {: ^15} {: ^15} {: ^14} {: ^14} {: ^8}  |\t {}\n"
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


def _dprinter(string, debug=False):
    if debug:
        print("DEBUG: {}".format(string))
    else:
        return


def check(args):
    if args.verbose == 1:
        verbose = True
        debug = False
    elif args.verbose >= 2:
        verbose = True
        debug = True
    else:
        verbose = False
        debug = False
    _dprinter("Starting LTO Check w/ DEBUG MODE ACTIVE", debug)
    _dprinter("Args detected:\nMaster CSV={}\nLTO CSV={}\nOutput Filepath={}\nOutput Filename={}\nVerbose Count={}"
              .format(args.master_csv_path, args.lto_csv_path, args.out_path,
                      args.out_name, args.verbose), debug)
    csv1 = args.master_csv_path
    csv2 = args.lto_csv_path

    try:
        _dprinter("Trying...", debug)
        master_media_files, count_mmf = _read_ss_csv(csv1, debug)
        lto_media_files, count_lmf = _read_lto_csv(csv2, debug)
        files_matched, files_non_matched, files_not_found = _compare_dicts(args, master_media_files,
                                                                           lto_media_files, verbose, debug)
        _summary_printer(count_mmf, count_lmf, files_matched, files_non_matched, files_not_found)
    except KeyboardInterrupt:
        _dprinter("Keyboard Interrupt Detected")
        sys.exit("Exiting...")
    except FileNotFoundError as e:
        _dprinter("File not found")
        sys.exit("File not found: {}\nExiting...".format(str(e).split("'")[-2]))
    except KeyError as e:
        _dprinter("Failed to find column")
        sys.exit('Failed to find column: {}'.format(e))
