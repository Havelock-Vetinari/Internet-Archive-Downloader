import os
from enum import Enum

from downloader.checksum import CheckSums, calculate_checksum


class FileValidation(Enum):
    OK = 0
    FILE_MISSING = 1
    INVALID = 2


def is_file_present_and_valid(path: str, file_name: str, sums: CheckSums):
    if not os.path.exists(path):
        return FileValidation.FILE_MISSING

    best_sum_type = sums.best_check_sum_type()
    best_sum_value = sums.get_check_sum_type(best_sum_type)
    calculated_checksum = calculate_checksum(path, best_sum_type)

    if calculated_checksum != best_sum_value:
        print("⚠️  File {} {} mismatch: got {} expected {}"
              .format(file_name, best_sum_type, calculated_checksum, best_sum_value))
        return FileValidation.INVALID
    else:
        print("👍  File {} found and checksum {} of type {} is ok".format(file_name, calculated_checksum, best_sum_type))
    return FileValidation.OK
