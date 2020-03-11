import filecmp
import glob
import os


class Helpers:
    @staticmethod
    def remove_files_in_output():
        files = glob.glob("tests/data/output/*")
        for file_name in files:
            if file_name != ".gitkeep":
                os.remove(file_name)

    @staticmethod
    def compare_files():
        files = glob.glob("tests/data/output/*.md")
        for file_name in files:
            expected_file = os.path.basename(file_name)
            expected_file_path = os.path.join("tests", "data", "expected", expected_file)
            assert filecmp.cmp(file_name, expected_file_path)
