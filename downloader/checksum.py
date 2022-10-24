import hashlib
import os
import zlib
from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union
from xml.dom.minidom import Element


class CheckSumTypes(Enum):
    SHA1 = 0
    MD5 = 1
    CRC32 = 2
    SIZE = 3


@dataclass
class CheckSums:
    sha1: Optional[str] = None
    md5: Optional[str] = None
    crc32: Optional[str] = None
    size: Optional[int] = None

    def best_check_sum_type(self) -> Optional[CheckSumTypes]:
        if self.sha1 is not None:
            return CheckSumTypes.SHA1
        if self.md5 is not None:
            return CheckSumTypes.MD5
        if self.crc32 is not None:
            return CheckSumTypes.CRC32
        if self.size is not None:
            return CheckSumTypes.SIZE
        return None

    def get_check_sum_type(self, checksum_type: CheckSumTypes) -> Union[str, int]:
        if checksum_type == CheckSumTypes.SHA1:
            return self.sha1
        if checksum_type == CheckSumTypes.MD5:
            return self.md5
        if checksum_type == CheckSumTypes.CRC32:
            return self.crc32
        if checksum_type == CheckSumTypes.SIZE:
            return self.sha1


def calculate_checksum(path: str, checksum_type: Optional[CheckSumTypes]) -> Union[str, int, None]:
    hash_alg = None
    if not os.path.isfile(path):
        return None
    if checksum_type is None:
        return None
    elif checksum_type == CheckSumTypes.SHA1:
        hash_alg = hashlib.sha1()
    elif checksum_type == CheckSumTypes.MD5:
        hash_alg = hashlib.md5()
    elif checksum_type == CheckSumTypes.CRC32:
        buffer_size = 65536
        with open(path, 'rb') as f:
            buffer = f.read(buffer_size)
            crc_value = 0
            while len(buffer) > 0:
                crc_value = zlib.crc32(buffer, crc_value)
                buffer = f.read(buffer_size)
        return format(crc_value & 0xFFFFFFFF, '08x')

    elif checksum_type == CheckSumTypes.SIZE:
        return os.path.getsize(path)

    with open(path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            hash_alg.update(byte_block)
        calculated_sha_sum = hash_alg.hexdigest()
    return calculated_sha_sum


def get_sums(file_node: Element) -> CheckSums:
    sums = CheckSums()
    sha1s = file_node.getElementsByTagName("sha1")
    if len(sha1s) > 0:
        sums.sha1 = sha1s[0].firstChild.data
    md5s = file_node.getElementsByTagName("md5")
    if len(md5s) > 0:
        sums.md5 = md5s[0].firstChild.data
    crc32s = file_node.getElementsByTagName("crc32")
    if len(crc32s) > 0:
        sums.crc32 = crc32s[0].firstChild.data
    sizes = file_node.getElementsByTagName("size")
    if len(sizes) > 0:
        sums.size = int(sizes[0].firstChild.data)
    return sums
