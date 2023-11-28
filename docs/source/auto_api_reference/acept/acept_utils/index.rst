:py:mod:`acept.acept_utils`
===========================

.. py:module:: acept.acept_utils

.. autoapi-nested-parse::

   Module containing utility functions for ACEPT



Module Contents
---------------


Functions
~~~~~~~~~

.. autoapisummary::

   acept.acept_utils.uppath
   acept.acept_utils.absolute_path_from_relative_posix
   acept.acept_utils.derive_output_path_from_filepath
   acept.acept_utils.copy_file_or_directory_recursively
   acept.acept_utils.rename_files_in_directory
   acept.acept_utils.delete_files_or_directory_recursively_with_pattern
   acept.acept_utils.combine_csv_profiles_with_pattern
   acept.acept_utils.concat_csv_profiles_columnwise
   acept.acept_utils.get_bid_from_uhp_building_specific_files



.. py:function:: uppath(filepath: str, n: int) -> str

   Climb directory path upwards

   :param filepath: Path to a file or directory
   :param n: Number of path levels to climb upwards
   :return: Path to the directory n levels upwards
   .. rubric:: Example

   >>> uppath("/parent/temp/dir/file.txt", 1)
   '/parent/temp/dir'


.. py:function:: absolute_path_from_relative_posix(posix_relative_to_src_files: str) -> str

   Returns the absolute path to the given relative POSIX path to a file or directory (relative to `/src/acept`)

   .. rubric:: Example

   >>> absolute_path_from_relative_posix("../../data/plz/plz-5stellig.shp")
   'path/to/the/acept/repository/data/plz/plz-5stellig.shp'

   :param posix_relative_to_src_files: Path to a file or directory, given as a POSIX path, relative to `/src/acept`.
   :return: Absolute path to the given path relative_to_src_files


.. py:function:: derive_output_path_from_filepath(output_base: str, filename: str, file_extension, mod_filename_suffix='_mod', up=1) -> str

   Derives output file path for modified file from input file path

   :param output_base: base directory path for modified files
   :param filename: path of input file
   :param file_extension: filename extension of input file e.g. '.shp'
   :param mod_filename_suffix: suffix for the modified filename before the filename extension. Default: '_mod'
   :param up: path levels above file. Default: 1 = Parent directory of input file
   :return: output path of modified shape file


.. py:function:: copy_file_or_directory_recursively(src_path: str, dst_path: str) -> str

   Copy file or directories including subdirectories and files recursively. The copying operation will continue
   if it encounters existing directories, and files within the dst tree will be overwritten by corresponding files
   from the src tree.

   :param src_path: Source path of the file or directory to copy
   :param dst_path: Destination path.


.. py:function:: rename_files_in_directory(path: str, old_substring: str, new_substring: str)

   Replace a sub string of all files names in a directory

   :param path: Path to the directory with the files.
   :param old_substring: Substring in filename to replace.
   :param new_substring: Substring to replace the old_substring with.


.. py:function:: delete_files_or_directory_recursively_with_pattern(directory: str, pattern: str)

   Deletes all files with the given pattern in the given directory

   :param directory: Path to the directory with the files
   :param pattern: Filename pattern of the files to delete


.. py:function:: combine_csv_profiles_with_pattern(src_directory: str, pattern: str, csv_profiles_path: str, new_header: list = None, key_function: callable = None, skip_rows: int = 0, column_name: str = None, in_delimiter: str = ';', debug: bool = False) -> pandas.DataFrame

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


.. py:function:: concat_csv_profiles_columnwise(file_1: str, file_2: str, output_file: str, in_delimiter_1: str = ';', in_delimiter_2: str = ';', out_delimiter: str = ';', add_index: bool = True)

   Appends file_2 to file_1 column-wise and writes the result to the CSV file output_file.

   :param file_1: Path to the first csv file
   :param file_2: Path to the second csv file
   :param output_file: Path to the output csv file
   :param in_delimiter_1: Delimiter of the first csv file
   :param in_delimiter_2: Delimiter of the second csv file
   :param out_delimiter: Delimiter of the output csv file
   :param add_index: Add an index to the output csv file


.. py:function:: get_bid_from_uhp_building_specific_files(filename: str) -> int

   Key function to extract the number after the last "_" in the filename for sorting.

   :param filename: Filename
   :return: Number after the last "_"


