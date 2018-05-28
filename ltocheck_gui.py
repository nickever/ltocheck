#!/usr/bin/env python3

"""
GUI tool to compare a master csv to an LTO csv.
Compares file size, frame quantity and MD5 Hash.
"""

# Import from Python Standard Library
import csv
import sys
import collections

# Import from the package


def _read_ss_csv(input_file):
    """
    Opens a SS csv as a dictionary with header as key, sorts by given column key, outputs filtered dictionary
    """
    print("Attempting master csv read")
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
    print("Master csv read and sorted from path {}\n{} files found, {} video files filtered"
              .format(input_file, len(reader), len(filtered_dict)))
    return filtered_dict, len(filtered_dict)


def _read_lto_csv(input_file):
    """
    Opens an LTO csv as a dictionary with header as key, sorts by given column key, outputs filtered dictionary
    """
    print("Attempting LTO csv read")
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
    print("LTO csv read and sorted from path {}\n{} files found, {} video files filtered"
              .format(input_file, len(reader), len(filtered_dict)))
    return filtered_dict, len(filtered_dict)


def _compare_dicts(ss_dict, lto_dict):
    """
    Compares two given dictionaries, returns quanity of matches, non matches and not found files
    as well as outputting data to the results printer func and csv creator
    """
    print("Attempting compare the csvs")
    match = 0
    non_match = 0
    not_found = 0
    results_dict = []
    for ss_row in ss_dict:
        file_found = False
        for lto_row in lto_dict:
            if ss_row['Name'] == lto_row['Name']:
                file_found = True
                match_status = ""
                error_message = ""
                if ss_row["Frames"] == lto_row["Frames"] \
                        and ss_row["Size"] == lto_row["Size"] \
                        and ss_row["MD5"].upper() == lto_row["MD5"].upper():
                    match += 1
                    match_status = "MATCH"
                else:
                    if ss_row["Frames"] != lto_row["Frames"]:
                        non_match += 1
                        match_status = "ERROR"
                        error_message += "FRAME COUNT MISMATCH \t"
                    if ss_row["Size"] != lto_row["Size"]:
                        non_match += 1
                        match_status = "ERROR"
                        error_message += "SIZE MISMATCH \t"
                    if ss_row["MD5"] != lto_row["MD5"]:
                        non_match += 1
                        match_status = "ERROR"
                        error_message += "MD5 MISMATCH \t"
                results_dict.append(collections.OrderedDict({'STATUS': match_status,
                                                             'FILENAME': ss_row['Name'],
                                                             'FRAMES_MASTER': ss_row['Frames'],
                                                             'FRAMES_LTO': lto_row['Frames'],
                                                             'SIZE_MASTER': ss_row['Size'],
                                                             'SIZE_LTO': lto_row['Size'],
                                                             'MD5_MASTER': ss_row['MD5'],
                                                             'MD5_LTO': lto_row['MD5'],
                                                             'LTO_TAPE': lto_row['Media'],
                                                             'ERROR MESSAGES': error_message}))
        if file_found is False:
            not_found += 1
            match_status = "ERROR"
            error_message = "FILE NOT FOUND"
            results_dict.append(collections.OrderedDict({'STATUS': match_status,
                                                         'FILENAME': ss_row['Name'],
                                                         'FRAMES_MASTER': ss_row['Frames'],
                                                         'SIZE_MASTER': ss_row['Size'],
                                                         'MD5_MASTER': ss_row['MD5'],
                                                         'ERROR MESSAGES': error_message}))
    return match, non_match, not_found, results_dict


first_write = True


def write_csv(output_filepath, results_dict):
    print("Attempting to write output csv to {}".format(output_filepath))
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
    writer = csv.DictWriter(output_filepath, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results_dict)
    output_filepath.close()


def results(int1, int2, int3, int4, int5):
    result = ("Total Video Files on Master: {}"
          "\nTotal Video Files on LTO: {}"
          "\nMatches: {}"
          "\nNon-Matches: {}"
          "\nNot Found: {}"
          .format(int1, int2, int3, int4, int5))
    return result


def check(csv1, csv2):
    print(csv1)
    print(csv2)
    try:
        master_media_files, count_mmf = _read_ss_csv(csv1)
        lto_media_files, count_lmf = _read_lto_csv(csv2)
        files_matched, files_non_matched, files_not_found, results_report = _compare_dicts(master_media_files,
                                                                                           lto_media_files)
        results_summary = results(count_mmf, count_lmf, files_matched, files_non_matched, files_not_found)
        return results_summary, results_report
    except KeyboardInterrupt:
        sys.exit("Exiting...")
    except FileNotFoundError as e:
        print("File not found: {}\nExiting...".format(str(e).split("'")[-2]))
    except KeyError as e:
        print('Failed to find column: {}'.format(e))


if __name__ == "__main__":      # executed when run from the command line
    check()
