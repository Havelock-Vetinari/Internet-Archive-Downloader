import unittest

from downloader.checksum import calculate_checksum, CheckSumTypes


class MyTestCase(unittest.TestCase):

    def test_calculating_sha1(self):
        self.assertEqual(
            first=calculate_checksum(path="sample_file.txt", checksum_type=CheckSumTypes.SHA1),
            second="f5d7d1099cb202ce533510f597c11cf19edcf361"
        )

    def test_calculating_md5(self):
        self.assertEqual(
            first=calculate_checksum(path="sample_file.txt", checksum_type=CheckSumTypes.MD5),
            second="c3166530944995a0780ea296c71fd15a"
        )

    def test_calculating_crc32(self):
        self.assertEqual(
            first=calculate_checksum(path="sample_file.txt", checksum_type=CheckSumTypes.CRC32),
            second="9ea95f7e"
        )


if __name__ == '__main__':
    unittest.main()
