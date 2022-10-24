from unittest import TestCase

from downloader.path_finder import get_archive_name, get_clean_file_path_parts, get_directory_path_from_parts


class Test(TestCase):
    def test_get_archive_name(self):
        self.assertEqual(
            first="sample-archive",
            second=get_archive_name("https://archive.org/details/sample-archive")
        )

    def test_get_archive_name_with_trailing_slash(self):
        self.assertEqual(
            first="sample-archive",
            second=get_archive_name("https://archive.org/details/sample-archive/")
        )

    def test_get_clean_file_path_parts(self):
        self.assertEqual(
            first=["dir1", "dir 2", "file 1.txt"],
            second=get_clean_file_path_parts("dir1/dir 2/file 1.txt")
        )

    def test_get_clean_file_path_parts_cleaning(self):
        self.assertEqual(
            first=["dir1", "dir 2", "file 1.txt"],
            second=get_clean_file_path_parts("../dir1/dir 2/./../file 1.txt")
        )

    def test_get_directory_path_from_parts(self):
        self.assertEqual(
            first=["dir1", "dir 2"],
            second=get_directory_path_from_parts(["dir1", "dir 2", "file 1.txt"])
        )

