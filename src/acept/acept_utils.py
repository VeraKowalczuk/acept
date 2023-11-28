"""Module containing utility functions for ACEPT"""

import errno
import glob
import os
import shutil

import pandas as pd


def uppath(filepath: str, n: int) -> str:
    """
    Climb directory path upwards

    :param filepath: Path to a file or directory
    :param n: Number of path levels to climb upwards
    :return: Path to the directory n levels upwards
    Example:
        >>> uppath("/parent/temp/dir/file.txt", 1)
        '/parent/temp/dir'
    """
    return os.sep.join(filepath.split(os.sep)[:-n])


def absolute_path_from_relative_posix(posix_relative_to_src_files: str) -> str:
    """
    Returns the absolute path to the given relative POSIX path to a file or directory (relative to `/src/acept`)

    Example:
        >>> absolute_path_from_relative_posix("../../data/plz/plz-5stellig.shp")
        'path/to/the/acept/repository/data/plz/plz-5stellig.shp'

    :param posix_relative_to_src_files: Path to a file or directory, given as a POSIX path, relative to `/src/acept`.
    :return: Absolute path to the given path relative_to_src_files
    """
    path_parts = posix_relative_to_src_files.split("/")

    return os.path.abspath(os.sep.join([os.path.dirname(__file__)] + path_parts))


def derive_output_path_from_filepath(output_base: str, filename: str, file_extension,
                                     mod_filename_suffix="_mod", up=1) -> str:
    """
    Derives output file path for modified file from input file path

    :param output_base: base directory path for modified files
    :param filename: path of input file
    :param file_extension: filename extension of input file e.g. '.shp'
    :param mod_filename_suffix: suffix for the modified filename before the filename extension. Default: '_mod'
    :param up: path levels above file. Default: 1 = Parent directory of input file
    :return: output path of modified shape file
    """
    input_base = uppath(filename, up)
    # filename_mod begins with / because uppath removes the last / in the input_base
    filename_mod = filename.removeprefix(input_base)
    filename_mod = filename_mod.removeprefix(os.sep)
    filename_mod = os.path.join(output_base,
                                f"{filename_mod[:-len(file_extension)]}{mod_filename_suffix}{file_extension}")
    return filename_mod


def copy_file_or_directory_recursively(src_path: str, dst_path: str) -> str:
    """
    Copy file or directories including subdirectories and files recursively. The copying operation will continue
    if it encounters existing directories, and files within the dst tree will be overwritten by corresponding files
    from the src tree.

    :param src_path: Source path of the file or directory to copy
    :param dst_path: Destination path.
    """
    print("Copy from", src_path, "to", dst_path)
    try:
        return shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
    except OSError as e:
        if e.errno in (errno.ENOTDIR, errno.EINVAL):
            # src_path is not a directory
            return shutil.copy(src_path, dst_path)
        else:
            raise


def rename_files_in_directory(path: str, old_substring: str, new_substring: str):
    """
    Replace a sub string of all files names in a directory

    :param path: Path to the directory with the files.
    :param old_substring: Substring in filename to replace.
    :param new_substring: Substring to replace the old_substring with.
    """
    for f in os.listdir(path):
        os.rename(os.path.join(path, f),
                  os.path.join(path, f.replace(old_substring, new_substring)))


def delete_files_or_directory_recursively_with_pattern(directory: str, pattern: str):
    """
    Deletes all files with the given pattern in the given directory

    :param directory: Path to the directory with the files
    :param pattern: Filename pattern of the files to delete
    """
    file_list = glob.glob(os.path.join(directory, pattern))
    for file_path in file_list:
        # print("Deleting", file_path)
        if os.path.isfile(file_path):
            os.remove(file_path)

        if os.path.isdir(file_path):
            shutil.rmtree(file_path)

        if os.path.isdir(file_path):
            os.rmdir(file_path)


def combine_csv_profiles_with_pattern(src_directory: str, pattern: str, csv_profiles_path: str,
                                      new_header: list = None, key_function: callable = None, skip_rows: int = 0,
                                      column_name: str = None, in_delimiter: str = ";",
                                      debug: bool = False) -> pd.DataFrame:
    """
    Combines all csv files with the given pattern in the given directory into a single csv file.

    :param src_directory: Path to the directory with the csv files
    :param pattern: Filename pattern of the csv files to combine
    :param csv_profiles_path: Path to the csv file to write the combined profile to
    :param new_header: New header for the combined profile
    :param key_function: Function to extract the number after the last "_" in the filename for sorting. If None,
        the files are sorted alphabetically.
    :param skip_rows: Number of rows to skip in the csv files
    :param column_name: Name of the column to extract from the csv files
    :param in_delimiter: Delimiter of the input csv files
    :param debug: Print debug information
    :return: Combined profile as pandas dataframe
    """
    # find all csv files with the given pattern
    csv_files = glob.glob(os.path.join(src_directory, pattern))
    if debug:
        print("Found", len(csv_files), "csv files with pattern", pattern, ":", csv_files)
    # sort the files by building ID in ascending order
    if key_function is not None:
        csv_files.sort(key=key_function)
    else:
        csv_files.sort()

    if column_name is not None:
        profiles_df_list = [
            pd.read_csv(f, skiprows=skip_rows, usecols=[column_name], index_col=False, delimiter=in_delimiter).rename(
                columns={column_name: new_header[i]}, inplace=False) for i, f
            in
            enumerate(csv_files)]
    else:
        profiles_df_list = [
            pd.read_csv(f, skiprows=skip_rows, names=[new_header[i]], index_col=False, delimiter=in_delimiter) for i, f
            in
            enumerate(csv_files)]

    combined_profile = pd.concat(profiles_df_list, axis="columns")
    combined_profile.to_csv(csv_profiles_path, index=False)
    return combined_profile


def concat_csv_profiles_columnwise(file_1: str, file_2: str, output_file: str, in_delimiter_1: str = ";",
                                   in_delimiter_2: str = ";", out_delimiter: str = ";", add_index: bool = True):
    """
    Appends file_2 to file_1 column-wise and writes the result to the CSV file output_file.

    :param file_1: Path to the first csv file
    :param file_2: Path to the second csv file
    :param output_file: Path to the output csv file
    :param in_delimiter_1: Delimiter of the first csv file
    :param in_delimiter_2: Delimiter of the second csv file
    :param out_delimiter: Delimiter of the output csv file
    :param add_index: Add an index to the output csv file
    """
    df1 = pd.read_csv(file_1, delimiter=in_delimiter_1, index_col=False)
    df1.set_index(df1.columns[0], inplace=True)
    df2 = pd.read_csv(file_2, delimiter=in_delimiter_2, index_col=False)
    df2.index = df1.index
    df_combined = pd.concat([df1, df2], axis="columns")
    df_combined.index.name = df1.index.name
    df_combined.to_csv(output_file, index=add_index, sep=out_delimiter)


# key function to extract the number after the last "_"
def get_bid_from_uhp_building_specific_files(filename: str) -> int:
    """
    Key function to extract the number after the last "_" in the filename for sorting.

    :param filename: Filename
    :return: Number after the last "_"
    """
    return int(filename.split('_')[-1].split('.')[0])
