import functools
import logging
import os
import shutil
from concurrent.futures import ThreadPoolExecutor

import click
import requests
from xml.dom import minidom

from downloader.checksum import calculate_checksum
from downloader.file import InternetArchiveFile
from downloader.file_validation import is_file_present_and_valid, FileValidation
from downloader.path_finder import get_archive_name, get_clean_file_path_parts, get_directory_path_from_parts


def download_file(base_url: str, file: InternetArchiveFile, folder_name: str):
    file_name_parts = get_clean_file_path_parts(file.name)
    local_file_dir = get_directory_path_from_parts(file_name_parts)
    path = os.path.join(folder_name, *file_name_parts)
    url = base_url + file.name
    with requests.get(url, stream=True) as r:
        file_dir_path = os.path.join(folder_name, *local_file_dir)
        if not os.path.exists(file_dir_path):
            os.makedirs(file_dir_path, exist_ok=True)
        with open(path, 'wb') as f:
            r.raw.read = functools.partial(r.raw.read, decode_content=True)
            shutil.copyfileobj(r.raw, f)

    if file.checksums is not None:
        best_sum_type = file.checksums.best_check_sum_type()
        best_sum_value = file.checksums.get_check_sum_type(best_sum_type)
        calculated_sha_sum = calculate_checksum(path, best_sum_type)

        if best_sum_value is not None and calculated_sha_sum != best_sum_value:
            print("⚠️  Invalid sum {} for file {}: got {} expected"
                  .format(best_sum_type, file.name, calculated_sha_sum, best_sum_value))
            return False
    return True


def process_file_for_downloading(file: InternetArchiveFile, base_url: str, folder_name: str):
    try:
        clean_path_parts = get_clean_file_path_parts(file.name)
        path = os.path.join(folder_name, *clean_path_parts)
        sums = file.checksums

        validation_result = is_file_present_and_valid(path=path, file_name=file.name, sums=sums)
        if validation_result == FileValidation.OK:
            print("⏭️  Skipping file {}".format(file.name))
            return
        elif validation_result == FileValidation.INVALID:
            os.remove(path)
            os.sync()
        print("🌏  Downloading file {} ...".format(file.name), flush=True)
        if download_file(base_url, file, folder_name):
            print("✅  OK {}".format(file.name), flush=True)
        else:
            print("❌  Failed {}".format(file.name), flush=True)
    except BaseException as e:
        logging.exception("An error occurred.", e)


@click.command()
@click.argument("url", type=click.STRING, required=True)
@click.option("--threads", type=click.INT, default=2, required=False)
@click.option("--target_dir", type=click.STRING, default="./", required=False)
def download_command(url, threads, target_dir):
    main(url, threads, target_dir)


def main(url, threads, target_dir):
    base_url = "https://archive.org/download/"
    archive_name = get_archive_name(url)
    archive_url = "{}{}/".format(base_url, archive_name)
    files_xml_name = "{}_files.xml".format(archive_name)
    download_file(archive_url, InternetArchiveFile(name=files_xml_name, checksums=None), target_dir)
    files = minidom.parse(os.path.join(target_dir, files_xml_name)).getElementsByTagName("file")
    pool = ThreadPoolExecutor(threads)
    for file in files:
        archive_file = InternetArchiveFile.from_element(file)
        if archive_file.name == files_xml_name:
            continue
        pool.submit(process_file_for_downloading, archive_file, archive_url, target_dir)


if __name__ == '__main__':
    download_command()
