import os
from itertools import repeat
from multiprocessing import Pool
from xml.dom import minidom

import click
from pathlib import Path

from downloader import checksum
from downloader.file import InternetArchiveFile


def validate_file(directory, file: InternetArchiveFile):
    path = os.path.join("{}/{}".format(directory, file.name))
    check_sums = file.checksums
    best_check_sum_type = check_sums.best_check_sum_type()
    if not os.path.exists(path):
        click.echo("⚠️ Missing file: {}".format(file.name))
    elif best_check_sum_type is not None:
        file_check_sum = checksum.calculate_checksum(path, checksum_type=best_check_sum_type)
        if file_check_sum != check_sums.get_check_sum_type(checksum_type=best_check_sum_type):
            click.echo("⚠️ Checksum mismatch (expected: {}, found: {}) for file {}"
                       .format(check_sums, file_check_sum, file.name)
                       )
        else:
            click.echo("✅ File is valid ({}): {}".format(best_check_sum_type, file.name))
    else:
        click.echo("❔ No checksum for file {}".format(file.name))


@click.command()
@click.argument("file_xml", nargs=1, type=click.File('r'))
@click.option("--directory", type=click.Path(exists=True, dir_okay=True, file_okay=False), default=Path.cwd(),
              required=False)
@click.option("--threads", type=click.INT, default=2, required=False)
def main(file_xml, directory, threads):
    files: map[InternetArchiveFile] = map(InternetArchiveFile.from_element,
                                          minidom.parse(file_xml).getElementsByTagName("file"))

    with Pool(threads) as pool:
        pool.starmap(validate_file, zip(repeat(directory), files))


if __name__ == '__main__':
    main()
