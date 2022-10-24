from dataclasses import dataclass
from typing import Union
from xml.dom.minidom import Element

from downloader.checksum import CheckSums, get_sums


@dataclass
class InternetArchiveFile:
    name: str
    checksums: Union[CheckSums, None]

    @classmethod
    def from_element(cls, element: Element):
        return cls(
            name=element.attributes["name"].value,
            checksums=get_sums(element)
        )
